import typing

from pyldplayer2.base.objects.appattr import AppAttr
from pyldplayer2.base.utils.wndlayout import grid_orientation
from pyldplayer2.coms.instanceQuery import Query
from pyldplayer2.coms.wndInstance import WndInstance


class GridLayoutOptions(typing.TypedDict):
    rows: int
    cols: int
    maxwidth: float | None = None
    maxheight: float | None = None
    minwidth: float | None = None
    minheight: float | None = None
    monitor: int = 0
    sleepTime: float = 0.2


def gridLayout(
    wnds: typing.List[WndInstance] | typing.Dict[int, WndInstance] | str,
    options: GridLayoutOptions,
    query: Query | AppAttr | None = None,
):
    if isinstance(wnds, str):
        wnds = WndInstance.query(
            wnds, query.attr if isinstance(query, Query) else query
        )

    if isinstance(wnds, dict):
        wnds = list(wnds.values())

    grid_orientation([wnd.wnd for wnd in wnds], **options)
