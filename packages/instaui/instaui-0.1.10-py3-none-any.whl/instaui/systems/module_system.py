from importlib import import_module
from types import ModuleType
from typing import Any, List


class LazyModule(ModuleType):
    def __init__(self, name: str, member: str):
        super().__init__(name)
        self._name = name
        self._mod = None
        self._member_obj = None
        self._member = member

    def __getattr__(self, attr: str) -> Any:
        self.__try_import()
        return getattr(self._member_obj, attr)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.__try_import()
        return self._member_obj(*args, **kwds)  # type: ignore

    def __dir__(self) -> List[str]:
        if self._mod is None:
            self._mod = import_module(self._name)
        return dir(self._mod)

    def __try_import(self):
        if self._mod is None:
            self._mod = import_module(self._name)
            self._member_obj = getattr(self._mod, self._member)
