import wx

from functions import Function


class InputImage(wx.ComboBox):
    # noinspection PyShadowingBuiltins
    def __init__(self, parent, id):
        choices = list(Function.get_all_vars().keys())
        super().__init__(parent, id, choices=choices, value=choices[0])

    def GetValue(self):
        return eval(super().GetValue(), Function.get_all_vars())
