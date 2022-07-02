from typing import Any, TYPE_CHECKING

import cv2
import wx
import numpy as np

from gui.basegui import WrapperBase
if TYPE_CHECKING:
    from functions import ParamType


# noinspection PyPep8Naming
class ControlWrapper(WrapperBase):
    def __init__(self, parent: wx.Window, tp: "ParamType", default: Any = None):
        from .control_factory import get_control_from_type
        super().__init__(parent, wx.ID_ANY)
        self.ctrl = get_control_from_type(self, tp, default)
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
        event.Skip()

    def SetValue(self, value: Any) -> None:
        self.ctrl.SetValue(value)

    def GetValue(self) -> Any:
        if self.toggle_code.GetValue():
            from gui.gui import MainFrame
            frame: MainFrame = self.GetTopLevelParent()
            env = {**frame.get_vars(self), "cv2": cv2, "np": np}
            return eval(self.code.GetValue(), env)
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

