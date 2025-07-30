from __future__ import annotations

import asyncio
import os
import sys
from dataclasses import dataclass
from inspect import signature
from os import PathLike
from pathlib import Path
from typing import Annotated, Any, Awaitable, Callable, Literal, Self, Union, cast

from pydantic import BaseModel, Discriminator, RootModel, Tag
from wasmtime import (
    Caller,
    Config,
    Engine,
    Func,
    FuncType,
    Instance,
    Linker,
    Memory,
    Store,
    Trap,
    ValType,
    WasiConfig,
)
from wasmtime import (
    Module as WasmModule,
)
from wasmtime._instance import InstanceExports


def pack_ptr(ptr: int, length: int) -> int:
    return (ptr << 32) | length

def unpack_ptr(packed: int) -> tuple[int, int]:
    return packed >> 32, packed & 0xFFFFFFFF


def get_obj_discriminator(value: Any) -> str:
    if isinstance(value, dict):
        return value.get("object", "")
    return getattr(value, "object", "")


class ModuleFeatureFlags(BaseModel):
    threads: bool = False
    tail_call: bool = False
    reference_types: bool = False
    simd: bool = False
    relaxed_simd: bool = False
    relaxed_simd_deterministic: bool = False
    bulk_memory: bool = False
    multi_value: bool = False
    multi_memory: bool = False
    memory64: bool = False


class ModuleLimits(BaseModel):
    memory_size: int = -1
    table_elements: int = -1
    instances: int = -1
    tables: int = -1
    memories: int = -1


class ModuleEnv(BaseModel):
    args: list[str] | None = None
    env: dict[str, Any] | None = None
    mount: dict[str, str] | None = None

    @classmethod
    def inherit(cls) -> ModuleEnv:
        return cls(
            args=sys.argv[1:],
            env=dict(os.environ),
            mount={
                "/tmp": os.path.join(os.getcwd(), "tmp"),
                "/var": os.path.join(os.getcwd(), "var"),
            },
        )


@dataclass
class FnError(Exception):
    message: str
    type: str

    def __str__(self):
        return f"{self.type}: {self.message}"


class FnResultData(BaseModel, extra="allow"):
    object: Literal["data"] = "data"
    value: Any | None = None


class FnResultError(BaseModel, extra="allow"):
    object: Literal["error"] = "error"
    type: str
    message: str


class FnResult(RootModel):
    root: Annotated[
        Union[
            Annotated[FnResultData, Tag("data")],
            Annotated[FnResultError, Tag("error")],
        ],
        Discriminator(get_obj_discriminator),
    ]


class FnInput(BaseModel):
    args: tuple[Any, ...] | None = None
    kwargs: dict[str, Any] | None = None


class ModuleFnWrapper:
    def __init__(
        self,
        name: str,
        instance: Instance,
        store: Store,
        memory: Memory,
        guest_alloc: Func,
        guest_dealloc: Func,
    ) -> None:
        self._name = name
        self._instance = instance
        self._store = store
        self._memory = memory
        self._guest_alloc = guest_alloc
        self._guest_dealloc = guest_dealloc

    def _write_memory(self, data: bytes) -> tuple[int, int]:
        data_len = len(data)
        data_ptr = self._guest_alloc(self._store, data_len)

        assert isinstance(data_ptr, int), "guest_alloc did not return an integer pointer"

        self._memory.write(self._store, data, data_ptr)
        return data_ptr, data_len

    def _read_memory(self, ptr: int, length: int) -> bytes:
        assert ptr and length, "Module function passed null pointer"

        try:
            return bytes(self._memory.read(self._store, ptr, ptr+length))
        finally:
            self._guest_dealloc(self._store, ptr, length)

    def _call_func(self, func: Func, input: bytes) -> bytes:
        input_ptr, input_len = self._write_memory(input)
        try:
            return self._read_memory(
                *unpack_ptr(
                    func(self._store, input_ptr, input_len)
                )
            )
        except Trap as e:
            raise RuntimeError(f"Module runtime error: {e}") from e
        finally:
            self._guest_dealloc(self._store, input_ptr, input_len)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        func = self._instance.exports(self._store).get(self._name)
        if func is None:
            raise AttributeError(f"Function '{self._name}' not found in Module.")

        fn_result = FnResult.model_validate_json(
            self._call_func(
                cast(Func, func),
                FnInput(args=args, kwargs=kwargs)
                .model_dump_json()
                .encode("utf-8"),
            )
        )

        if isinstance(fn_result.root, FnResultError):
            raise FnError(
                message=fn_result.root.message,
                type=fn_result.root.type,
            )
        elif isinstance(fn_result.root, FnResultData):
            return fn_result.root.value
        else:
            raise RuntimeError(
                f"Unexpected result type: {type(fn_result.root)}",
            )


class HostFnWrapper:
    def __init__(
        self,
        func: Callable[..., Any],
    ) -> None:
        self._func = func
        self._signature = signature(func)
        self.__store: Store | None = None
        self.__memory: Memory | None = None
        self.__guest_alloc: Func | None = None
        self.__guest_dealloc: Func | None = None

    def bind(
        self,
        store: Store,
        memory: Memory,
        guest_alloc: Func,
        guest_dealloc: Func,
    ) -> None:
        self.__store = store
        self.__memory = memory
        self.__guest_alloc = guest_alloc
        self.__guest_dealloc = guest_dealloc

    @property
    def _store(self) -> Store:
        assert self.__store is not None, "Host function not bound to store"
        return self.__store

    @property
    def _memory(self) -> Memory:
        assert self.__memory is not None, "Host function not bound to memory"
        return self.__memory

    def _guest_alloc(self, size: int) -> int:
        assert self.__guest_alloc is not None, "Host function not bound to guest_alloc"
        return self.__guest_alloc(self._store, size)

    def _guest_dealloc(self, ptr: int, size: int) -> None:
        assert self.__guest_dealloc is not None, "Host function not bound to guest_dealloc"
        self.__guest_dealloc(self._store, ptr, size)

    def _read_memory(self, ptr: int, length: int) -> bytes:
        assert ptr and length, "Module function passed null pointer"

        return bytes(self._memory.read(self._store, ptr, ptr+length))

    def _write_memory(self, data: bytes) -> tuple[int, int]:
        data_len = len(data)
        data_ptr = self._guest_alloc(data_len)

        assert isinstance(data_ptr, int), "guest_alloc did not return an integer pointer"

        self._memory.write(self._store, data, data_ptr)
        return data_ptr, data_len

    def __call__(self, caller: Caller, ptr: int) -> int:
        try:
            fn_input = FnInput.model_validate_json(
                self._read_memory(
                    *unpack_ptr(ptr)
                )
            )

            result_ptr, result_len = self._write_memory(
                FnResult(
                    root=FnResultData(
                        value=self._func(
                            *(fn_input.args or ()),
                            **(fn_input.kwargs or {}),
                        ),
                    )
                )
                .model_dump_json()
                .encode("utf-8"),
            )
            return pack_ptr(result_ptr, result_len)
        except Exception as e:
            error_ptr, error_len = self._write_memory(
                FnResult(
                    root=FnResultError(
                        type=type(e).__name__,
                        message=str(e)
                    )
                )
                .model_dump_json()
                .encode("utf-8"),
            )
            return pack_ptr(error_ptr, error_len)


class _ModuleAPIProxy:
    def __init__(
        self,
        instance: Instance,
        store: Store,
        memory: Memory,
        guest_alloc: Func,
        guest_dealloc: Func,
    ) -> None:
        self._instance = instance
        self._store = store
        self._memory = memory
        self._guest_alloc = guest_alloc
        self._guest_dealloc = guest_dealloc


class SyncModuleAPIProxy(_ModuleAPIProxy):
    def __getattr__(self, name: str) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return ModuleFnWrapper(
                name=name,
                instance=self._instance,
                store=self._store,
                memory=self._memory,
                guest_alloc=self._guest_alloc,
                guest_dealloc=self._guest_dealloc,
            )(
                *args, **kwargs
            )
        return wrapper


class AsyncModuleAPIProxy(_ModuleAPIProxy):
    def __getattr__(self, name: str) -> Callable[..., Awaitable[Any]]:
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            return await asyncio.to_thread(
                ModuleFnWrapper(
                    name=name,
                    instance=self._instance,
                    store=self._store,
                    memory=self._memory,
                    guest_alloc=self._guest_alloc,
                    guest_dealloc=self._guest_dealloc,
                ),
                *args, **kwargs
            )
        return wrapper


class Module:
    def __init__(
        self,
        binary: bytes,
        name: str,
        environment: ModuleEnv | None = None,
        namespace: str | None = None,
        host_fns: dict[str, Callable[..., Any]] | None = None,
        compilation_strategy: Literal["auto", "cranelift"] = "auto",
        feature_flags: ModuleFeatureFlags | None = None,
        limits: ModuleLimits | None = None,
        modules: list[Module] | None = None,
        cache: bool = False,
        epoch_interruption: bool = False,
        consume_fuel: bool = False,
        fuel: int = 0,
    ) -> None:
        self._name = name
        self._namespace = namespace or "env"
        self._binary = binary
        self._environment = environment or ModuleEnv.inherit()
        self._host_fns = host_fns or {}
        self._host_fn_wrappers: dict[str, HostFnWrapper] = {}
        self._modules = modules or []
        self._linked_modules: set[str] = set()

        self._config = self._build_config(
            compilation_strategy=compilation_strategy,
            feature_flags=feature_flags,
            cache=cache,
            epoch_interruption=epoch_interruption,
            consume_fuel=consume_fuel,
        )
        self._engine = Engine(self._config)
        self._store = Store(self._engine)
        self._linker = Linker(self._engine)
        self._module = WasmModule(self._engine, binary)
        self._instance: Instance | None = None
        self._exports: InstanceExports | None = None
        self._memory: Memory | None = None
        self._guest_alloc: Func | None = None
        self._guest_dealloc: Func | None = None

        if limits:
            self._store.set_limits(
                memory_size=limits.memory_size,
                table_elements=limits.table_elements,
                instances=limits.instances,
                tables=limits.tables,
                memories=limits.memories,
            )
        if fuel:
            self._store.set_fuel(fuel)

        for module in self._modules:
            self.link_module(module)

    def _build_config(
        self,
        compilation_strategy: Literal["auto", "cranelift"] = "auto",
        feature_flags: ModuleFeatureFlags | None = None,
        cache: bool = False,
        epoch_interruption: bool = False,
        consume_fuel: bool = False,
    ) -> Config:
        config = Config()
        config.epoch_interruption = epoch_interruption
        config.consume_fuel = consume_fuel

        if feature_flags:
            config.wasm_threads = feature_flags.threads
            config.wasm_tail_call = feature_flags.tail_call
            config.wasm_reference_types = feature_flags.reference_types
            config.wasm_simd = feature_flags.simd
            config.wasm_bulk_memory = feature_flags.bulk_memory
            config.wasm_multi_value = feature_flags.multi_value
            config.wasm_multi_memory = feature_flags.multi_memory
            config.wasm_memory64 = feature_flags.memory64

        config.strategy = compilation_strategy

        # Note: Caching can not be explicitly disabled so we only
        # set the var if it is True.
        if cache:
            config.cache = cache

        return config

    def _build_env(
        self,
        environment: ModuleEnv | None = None,
    ) -> None:
        wasi = WasiConfig()

        if environment and environment.args:
            wasi.argv = environment.args
        if environment and environment.env:
            wasi.env = list(environment.env.items())
        if environment and environment.mount:
            for guest_path, host_path in environment.mount.items():
                wasi.preopen_dir(guest_path, host_path)

        wasi.inherit_stdout()
        wasi.inherit_stderr()

        self._linker.define_wasi()
        self._store.set_wasi(wasi)

    def _register_host_fn(self, name: str, func: Callable[..., Any]) -> None:
        self._host_fn_wrappers[name] = HostFnWrapper(func)

        self._linker.define(
            store=self._store,
            module=self._namespace,
            name=name,
            item=Func(
                store=self._store,
                ty=FuncType(
                    params=[ValType.i64()],
                    results=[ValType.i64()],
                ),
                func=self._host_fn_wrappers[name],
                access_caller=True,
            )
        )

    def _register_host_fns(
        self,
        host_fns: dict[str, Callable[..., Any]] | None = None,
    ) -> None:
        assert (
            self._guest_alloc is not None
            and self._guest_dealloc is not None
        ), "Module not instantiated or missing required components"

        # Because type narrowing doesn't propagate to the lambda
        # functions
        guest_alloc = self._guest_alloc
        guest_dealloc = self._guest_dealloc

        self._linker.define(
            store=self._store,
            module=self._namespace,
            name="host_alloc",
            item=Func(
                store=self._store,
                ty=FuncType(
                    params=[ValType.i32()],
                    results=[ValType.i32()],
                ),
                func=lambda size: guest_alloc(self._store, size),
                access_caller=False
            )
        )
        self._linker.define(
            store=self._store,
            module=self._namespace,
            name="host_dealloc",
            item=Func(
                store=self._store,
                ty=FuncType(
                    params=[ValType.i32(), ValType.i32()],
                    results=[],
                ),
                func=lambda ptr, size: guest_dealloc(self._store, ptr, size),
                access_caller=False
            )
        )

        if host_fns:
            for name, func in host_fns.items():
                self._register_host_fn(name, func)

    def _add_module(self, module: Module) -> None:
        if module.name in [m.name for m in self._modules]:
            return

        self._modules.append(module)

    def _link_module(self, module: Module) -> None:
        if not module._instance or module.name in self._linked_modules:
            return

        self._linker.define_instance(
            store=self._store,
            name=module.name,
            instance=module._instance,
        )
        self._linked_modules.add(module.name)

    @property
    def instantiated(self) -> bool:
        return self._instance is not None

    @property
    def name(self) -> str:
        return self._name

    @property
    def api(self) -> SyncModuleAPIProxy:
        assert (
            self._instance is not None
            and self._store is not None
            and self._memory is not None
            and self._guest_alloc is not None
            and self._guest_dealloc is not None
        ), "Module not instantiated or missing required components"

        return SyncModuleAPIProxy(
            instance=self._instance,
            store=self._store,
            memory=self._memory,
            guest_alloc=self._guest_alloc,
            guest_dealloc=self._guest_dealloc,
        )

    @property
    def async_api(self) -> AsyncModuleAPIProxy:
        assert (
            self._instance is not None
            and self._store is not None
            and self._memory is not None
            and self._guest_alloc is not None
            and self._guest_dealloc is not None
        ), "Module not instantiated or missing required components"

        return AsyncModuleAPIProxy(
            instance=self._instance,
            store=self._store,
            memory=self._memory,
            guest_alloc=self._guest_alloc,
            guest_dealloc=self._guest_dealloc,
        )

    @classmethod
    def from_file(
        cls,
        file_path: Path | str | PathLike,
        name: str,
        environment: ModuleEnv | None = None,
        namespace: str | None = None,
        host_fns: dict[str, Callable[..., Any]] | None = None,
        compilation_strategy: Literal["auto", "cranelift"] = "auto",
        feature_flags: ModuleFeatureFlags | None = None,
        limits: ModuleLimits | None = None,
        cache: bool = False,
        epoch_interruption: bool = False,
        consume_fuel: bool = False,
        fuel: int = 0,
    ) -> Module:
        return cls(
            binary=Path(file_path).read_bytes(),
            name=name,
            environment=environment,
            namespace=namespace,
            host_fns=host_fns,
            compilation_strategy=compilation_strategy,
            feature_flags=feature_flags,
            limits=limits,
            cache=cache,
            epoch_interruption=epoch_interruption,
            consume_fuel=consume_fuel,
            fuel=fuel,
        )

    def __add__(self, other: Module) -> Self:
        return self.add_module(other)

    def add_module(self, module: Module) -> Self:
        assert not self.instantiated, "Cannot add modules after instantiation"

        if not isinstance(module, Module):
            raise TypeError("Module must be an instance of Module")

        self._add_module(module)
        return self

    def link_module(self, module: Module) -> Self:
        assert not self.instantiated, "Cannot link modules after instantiation"
        assert module.instantiated and module._instance, "Linked module must be instantiated"
        assert module.name not in self._linked_modules, "Module already linked"

        if not isinstance(module, Module):
            raise TypeError("Module must be an instance of Module")

        self._link_module(module)
        return self

    def instantiate(self) -> Self:
        assert not self.instantiated, "Module already instantiated"

        for module in self._modules:
            if not module.instantiated:
                module.instantiate()

            self._link_module(module)

        self._build_env(environment=self._environment)

        self._instance = self._linker.instantiate(self._store, self._module)
        self._exports = self._instance.exports(self._store)
        self._memory = cast(Memory, self._exports["memory"])
        self._guest_alloc = cast(Func, self._exports["guest_alloc"])
        self._guest_dealloc = cast(Func, self._exports["guest_dealloc"])

        for host_fn in self._host_fn_wrappers.values():
            host_fn.bind(
                store=self._store,
                memory=self._memory,
                guest_alloc=self._guest_alloc,
                guest_dealloc=self._guest_dealloc,
            )

        self._register_host_fns(host_fns=self._host_fns)
        return self

    def get_fuel(self) -> int:
        return self._store.get_fuel()

    def set_fuel(self, fuel: int) -> Self:
        self._store.set_fuel(fuel)
        return self

    def set_epoch_deadline(self, epoch_deadline: bool) -> Self:
        self._store.set_epoch_deadline(epoch_deadline)
        return self
