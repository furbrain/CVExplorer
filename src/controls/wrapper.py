from typing import Any

import wx

from functions import ParamType
from gui.basegui import WrapperBase


# noinspection PyPep8Naming
class ControlWrapper(WrapperBase):
    def __init__(self, parent: wx.Window, tp: ParamType):
        from .control_factory import get_control_from_type
        super().__init__(parent, wx.ID_ANY)
        self.ctrl = get_control_from_type(self, tp)
        self.ctrl.Reparent(self)
        self.sizer.Add(self.ctrl, 1, wx.ALL, 3)
        self.sizer.Fit(self)
        self.Layout()

    def show_code(self, event):
        if self.toggle_code.GetValue():
            self.code.Show()
            self.ctrl.Hide()
        else:
            self.code.Hide()
            self.ctrl.Show()
        self.sizer.Fit(self)
        self.Layout()

    def SetValue(self, value: Any) -> None:
        self.ctrl.SetValue(value)

    def GetValue(self) -> Any:
        if self.toggle_code.GetValue():
            from functions import Function
            return eval(self.code.GetValue(), Function.get_all_vars())
        else:
            return self.ctrl.GetValue()

    def GetCode(self) -> str:
        if self.toggle_code.GetValue():
            return self.code.GetValue()
        else:
            return self.ctrl.GetCode()

    def SetToolTip(self, text: str):
        self.toggle_code.SetToolTip(text)
        self.code.SetToolTip(text)
        self.ctrl.SetToolTip(text)

