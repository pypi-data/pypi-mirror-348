from pyldplayer2.base.objects.appattr import AppAttr
from pyldplayer2.coms.instanceQuery import Query
import pygetwindow as gw
from pyldplayer2.base.utils.wnd import activate_wnd

try:
    import pyautogui as pg
except ImportError:

    class _pg:
        def __getattr__(self, x: str):
            raise ImportError("pyautogui is not installed")
            return self

        def __call__(self, *args, **kwargs):
            raise ImportError("pyautogui is not installed")
            return self

    pg = _pg()


class WndInstanceMeta(type):
    _instances: dict[AppAttr, dict[int, "WndInstance"]] = {}

    def __call__(cls, query: Query, id: int, wnd: gw.Win32Window | None = None):
        if cls._instances.get(query.attr) is None:
            cls._instances[query.attr] = {}
        cls._instances[query.attr][id] = super().__call__(query, id, wnd)
        return cls._instances[query.attr][id]

    def refresh(cls, query: Query):
        metas = query.query("running")
        metanames = [meta["name"] for meta in metas]
        allwnds: list[gw.Win32Window] = gw.getAllWindows()
        allwnds = {
            wnd._hWnd: wnd
            for wnd in allwnds
            if wnd.width > 0 and wnd.height > 0 and wnd.title in metanames
        }
        if cls._instances.get(query.attr) is None:
            cls._instances[query.attr] = {}

        instancemap = cls._instances[query.attr]
        modified = []
        for meta in metas:
            if instancemap.get(meta["id"]) is None:
                instancemap[meta["id"]] = cls(
                    query, meta["id"], allwnds[meta["top_window_handle"]]
                )
            else:
                instancemap[meta["id"]]._WndInstance__wnd = allwnds[
                    meta["top_window_handle"]
                ]
            modified.append(instancemap[meta["id"]])

        # get non modified
        nonmodified = [
            instance for instance in instancemap.values() if instance not in modified
        ]
        for instance in nonmodified:
            instance.disabled = True

    def reset(cls, query: Query | None = None):
        if query is None:
            cls._instances = {}
        elif query.attr in cls._instances:
            cls._instances[query.attr] = {}
        else:
            raise ValueError("query not found")


class WndInstance(metaclass=WndInstanceMeta):
    @classmethod
    def query(
        cls, query: str | None = None, attr: AppAttr | None = None
    ) -> dict[int, "WndInstance"]:
        attr = attr or AppAttr.default()
        assert isinstance(attr, AppAttr), "attr not specified"
        qobj = Query(attr)
        cls.refresh(qobj)

        q = qobj.queryInts(query)
        return {id: cls._instances[attr][id] for id in q}

    def __init__(self, query: Query, id: int, wnd: gw.Win32Window | None = None):
        self.__query = query
        self.__id = id
        self.__wnd = wnd
        assert self.__id and isinstance(self.__id, int), "init using query"
        assert self.__wnd and isinstance(self.__wnd, gw.Win32Window), "init using query"
        assert self.__query and isinstance(self.__query, Query), "init using query"
        assert self.__query.attr.isValid, "init using query"

    @property
    def disabled(self) -> bool:
        return self.__wnd is None

    @disabled.setter
    def disabled(self, value: bool):
        if value:
            self.__wnd = None
        else:
            raise ValueError("disabled cannot be set to True")

    def __del__(self):
        self.__class__._instances.get(self.__query.attr).pop(self.__id)

    def __getattr__(self, name: str):
        if name == "disabled" or name.startswith("_"):
            return super().__getattribute__(name)

        if self.disabled:
            raise AttributeError(f"{name} is not available when disabled")

        return getattr(self.__wnd, name)

    @property
    def wnd(self) -> gw.Win32Window:
        return self.__wnd

    def focus(self):
        activate_wnd(self.__wnd)

    # automations
    def volumeup(self):
        self.focus()
        with pg.hold("ctrl"):
            pg.press("+")

    def volumedown(self):
        self.focus()
        with pg.hold("ctrl"):
            pg.press("-")

    def volumeMute(self):
        self.focus()
        with pg.hold("ctrl"):
            for _ in range(20):
                pg.press("-")

    def screenshot(self):
        self.focus()
        with pg.hold("ctrl"):
            pg.press("0")

    def shake(self):
        self.focus()
        with pg.hold("ctrl"):
            pg.press("6")

    def virtualGps(self):
        self.focus()
        with pg.hold("ctrl"):
            pg.press("7")

    def volumeMax(self):
        self.focus()
        with pg.hold("ctrl"):
            for _ in range(20):
                pg.press("+")

    def installApkDialog(self):
        self.focus()
        with pg.hold("ctrl"):
            pg.press("i")

    def sharedFolder(self):
        self.focus()
        with pg.hold("ctrl"):
            pg.press("5")

    def fullscreen(self):
        self.focus()
        pg.press("f11")

    def operationRecorder(self):
        self.focus()
        with pg.hold("ctrl"):
            pg.press("8")

    def synchronizer(self):
        self.focus()
        with pg.hold("ctrl"):
            pg.press("9")
