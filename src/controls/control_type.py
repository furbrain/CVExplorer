from typing import Protocol, Any

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


class InnerParamControl(ParamControl, Protocol):

    # noinspection PyUnusedLocal,PyShadowingBuiltins
    def __init__(self, parent: wx.Window, id: int):
        ...
