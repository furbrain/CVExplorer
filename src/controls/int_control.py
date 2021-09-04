from typing import Any

import wx


class IntSpin(wx.SpinCtrl):
    def __init__(self, *args, **kw):
        if "min" not in kw:
            kw["min"] = -1
        super().__init__(*args, **kw)

    def SetValue(self, value: Any):
        super().SetValue(str(value))

    def GetValue(self) -> Any:
        return int(super().GetValue())
