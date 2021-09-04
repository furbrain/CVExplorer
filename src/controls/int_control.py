from typing import Any

import wx


class IntSpin(wx.SpinCtrl):

    def SetValue(self, value: Any):
        super().SetValue(str(value))

    def GetValue(self) -> Any:
        return int(super().GetValue())
