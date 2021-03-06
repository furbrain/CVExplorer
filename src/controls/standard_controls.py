from typing import Any

import wx
from wx.lib.agw.floatspin import FloatSpin


# noinspection PyPep8Naming
class IntControl(wx.SpinCtrl):
    def __init__(self, *args, **kw):
        if "min" not in kw:
            kw["min"] = -(10**10)
        if "max" not in kw:
            kw["max"] = 10 ** 10
        super().__init__(*args, **kw)

    def SetValue(self, value: Any):
        super().SetValue(str(value))

    def GetValue(self) -> Any:
        return int(super().GetValue())

    def GetCode(self):
        return str(self.GetValue())


# noinspection PyPep8Naming
class FloatControl(FloatSpin):
    def GetCode(self):
        return f"{self.GetValue():.3g}"


# noinspection PyPep8Naming
class BoolControl(wx.CheckBox):
    def GetCode(self):
        return repr(bool(self.GetValue()))


# noinspection PyPep8Naming
class TextControl(wx.TextCtrl):
    def GetCode(self):
        return repr(self.GetValue())
