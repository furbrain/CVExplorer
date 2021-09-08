from typing import Protocol, Any

import wx

from .array_control import ArrayControl
from .standard_controls import IntControl, FloatControl, BoolControl, TextControl
from .point_control import PointControl
from .size_control import SizeControl
from .term_criteria_control import TermCriteriaControl
from .scalar_control import ScalarControl


# noinspection PyPep8Naming
class ParamControl(Protocol):
    # noinspection PyUnusedLocal,PyShadowingBuiltins
    def __init__(self, parent: wx.Window, id: int):
        ...

    def SetValue(self, value: Any) -> None:
        ...

    def GetValue(self) -> Any:
        ...

    def GetCode(self) -> str:
        ...

    def SetToolTip(self, text: str) -> None:
        ...
