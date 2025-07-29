from functools import cached_property
import os
import subprocess
import typing


class AppAttrMeta(type):
    _default: "AppAttr" = None
    _last: "AppAttr" = None
    _instances: dict[str, "AppAttr"] = {}

    def __call__(cls, path: str | None = None):
        if path is None and cls._default is not None:
            return cls._default

        if not os.path.exists(path):
            raise FileNotFoundError(f"AppAttrMeta: {path} not found")

        if not os.path.isdir(path):
            raise NotADirectoryError(f"AppAttrMeta: {path} is not a directory")

        if path in cls._instances:
            return cls._instances[path]

        path = os.path.abspath(path)

        ins = super().__call__(path)
        cls._instances[path] = ins
        cls._last = ins

        if cls._default is None:
            cls._default = ins

        return ins


class AppAttr(metaclass=AppAttrMeta):
    def __eq__(self, other: "AppAttr"):
        return self.path == other.path

    def __hash__(self):
        return hash(self.path)

    @classmethod
    def default(cls) -> "AppAttr":
        if cls._default is None:
            return None
        return cls._default

    @classmethod
    def last(cls) -> "AppAttr":
        if cls._last is None:
            return None
        return cls._last

    @classmethod
    def clearDefault(cls):
        cls._default = None

    def __init__(self, path: str):
        self.path = path

    @cached_property
    def dnconsole(self) -> str:
        return os.path.join(self.path, "dnconsole.exe")

    @cached_property
    def ldconsole(self) -> str:
        return os.path.join(self.path, "ldconsole")

    @cached_property
    def vmfolder(self) -> str:
        return os.path.join(self.path, "vms")

    @cached_property
    def customizeConfigs(self) -> str:
        return os.path.join(self.vmfolder, "customizeConfigs")

    @cached_property
    def recommendedConfigs(self) -> str:
        return os.path.join(self.vmfolder, "recommendConfigs")

    @cached_property
    def operationRecords(self) -> str:
        return os.path.join(self.vmfolder, "operationRecords")

    @cached_property
    def config(self) -> str:
        return os.path.join(self.vmfolder, "config")

    @property
    def isValid(self) -> bool:
        s = subprocess.run(self.ldconsole, capture_output=True, text=True)
        code = s.returncode

        return all(
            [
                os.path.exists(self.dnconsole),
                os.path.exists(self.vmfolder),
                os.path.exists(self.customizeConfigs),
                os.path.exists(self.recommendedConfigs),
                os.path.exists(self.operationRecords),
                os.path.exists(self.config),
                code == 0,
            ]
        )


class UseAppAttrMeta(type):
    _instances: dict[AppAttr, typing.Dict[typing.Type, "UseAppAttr"]] = {}

    def __call__(cls, path: str | AppAttr | None = None, *args, **kwargs):
        if path is None:
            path = AppAttr.default()

        if not isinstance(path, AppAttr):
            path = AppAttr(path)

        if path not in cls._instances:
            cls._instances[path] = {}

        if cls in cls._instances[path]:
            return cls._instances[path][cls]

        ins = super().__call__(path, *args, **kwargs)
        cls._instances[path][cls] = ins
        return ins


class UseAppAttr(metaclass=UseAppAttrMeta):
    attr: AppAttr

    def __init__(self, path: str | AppAttr | None = None, checkValid: bool = True):
        self.attr: AppAttr = path
        if checkValid:
            assert self.attr.isValid, "UseAppAttr: appattr is not valid"

        self.__ld_post_init__()

    def __ld_post_init__(self):
        pass
