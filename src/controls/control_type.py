from typing import Protocol, Any, Dict, Callable

import wx


# noinspection PyUnusedLocal,PyPep8Naming
class ParamControl(Protocol):

    def SetValue(self, value: Any) -> None:
        ...

    def GetValue(self) -> Any:
        ...

    def GetCode(self) -> str:
        ...

    def SetToolTip(self, text: str) -> None:
        ...

    def Show(self, show=True) -> None:
        ...

    def Hide(self) -> None:
        ...

    def Reparent(self, parent: wx.Window) -> None:
        ...

    def Bind(self, event: int, func: Callable) -> None:
        ...


class InnerParamControl(ParamControl, Protocol):

    # noinspection PyUnusedLocal,PyShadowingBuiltins
    def __init__(self, parent: wx.Window, id: int):
        ...


ParamsInstance = Dict[str, ParamControl]
