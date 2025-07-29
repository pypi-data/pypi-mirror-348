from contextlib import contextmanager
import typing
from pyldplayer2.base.objects.appattr import UseAppAttr
from pyldplayer2.coms.console import Console
from pyldplayer2.base.objects.iconsole import IConsole
import pyldplayer2.base.enums.console as E
from pyldplayer2.coms.instanceQuery import ALL_QUERY_TYPES, Query
import time


class BatchConsole(UseAppAttr, IConsole):
    """Batch console for managing multiple LDPlayer instances.
    easily extensible, simply extend the BatchConsole class and override the _batch or batch method accordingly

    Example:
        # Launch multiple instances with 5s interval
        batch = BatchConsole()
        batch.setScope([1, 2, 3])  # Target instances 1, 2, and 3
        batch.launch()  # Will launch each instance with 5s delay

    Note:
        - Commands must be in BATCHABLE_COMMANDS
        - Default interval: 5s
        - Default timeout: 500s (0 = no timeout)
    """

    def __ld_post_init__(self):
        self.__console = Console(self.attr)
        self.__scope = Query(self.attr).queryInts("all")
        self.__toggle = True
        self.__interval = 5
        self.__timeout = 500

    @property
    def timeout(self):
        return self.__timeout

    @timeout.setter
    def timeout(self, value: int):
        self.__timeout = value

    @property
    def interval(self):
        return self.__interval

    @interval.setter
    def interval(self, value: int):
        if not isinstance(value, int):
            raise ValueError("Interval must be an integer")
        self.__interval = value

    @contextmanager
    def asbatch(self, toggle: bool = True):
        previous = self.__toggle
        self.__toggle = toggle
        yield
        self.__toggle = previous

    def __getattribute__(self, key: str):
        if key.startswith("_"):
            return super().__getattribute__(key)
        if key in E.BATCHABLE_COMMANDS and self.__toggle:
            return self.__batch_command(key)
        if key in E.FULL_COMMANDS_LIST:
            return getattr(self.__console, key)
        return super().__getattribute__(key)

    def setScope(self, scope: ALL_QUERY_TYPES):
        self.__scope = Query(self.attr).queryInts(scope)

    @property
    def scope(self) -> typing.List[int]:
        return list(self.__scope)

    def __batch_command(self, command: str):
        def wrapper(*args, **kwargs):
            return self._batch(
                self.__console,
                command,
                self.__scope,
                self.__interval,
                self.__timeout,
                *args,
                **kwargs,
            )

        return wrapper

    @classmethod
    def _batch(
        cls,
        console: IConsole,
        command: str,
        scope: typing.List[int],
        interval: int = 5,
        timeout: int = 500,
        *args,
        **kwargs,
    ):
        """
        batch with all checks skipped
        """
        method = getattr(console, command)
        assert callable(method), f"Command {command} is not callable"
        for i in scope:
            method(index=i, *args, **kwargs)
            time.sleep(interval)
            if timeout > 0:
                timeout -= interval
                if timeout <= 0:
                    break

    @classmethod
    def batch(
        cls,
        console: IConsole,
        command: str,
        scope: ALL_QUERY_TYPES,
        interval: int = 5,
        timeout: int = 500,
    ):
        if command not in E.BATCHABLE_COMMANDS:
            raise ValueError(f"Command {command} is not batchable")

        if not isinstance(scope, list) and not isinstance(scope, int):
            scope = Query(console.attr).queryInts(scope)
        if not isinstance(interval, int):
            raise ValueError("Interval must be an integer")
        if not isinstance(timeout, int):
            raise ValueError("Timeout must be an integer")

        return cls._batch(console, command, scope, interval, timeout)
