from typing import Optional

import wx


class ArrayControl(wx.ComboBox):
    # noinspection PyShadowingBuiltins
    def __init__(self, parent, id):
        from functions import Function
        choices = list(Function.get_all_vars().keys())
        super().__init__(parent, id, choices=choices, value=choices[0])

    def SetValue(self, value: Optional[str]):
        if value is None:
            self.SetSelection(0)
        else:
            super().SetValue(value)

    def GetValue(self):
        from functions import Function
        return eval(super().GetValue(), Function.get_all_vars())
