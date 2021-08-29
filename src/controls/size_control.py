import wx

from controls import IntSpin


class SizeControl(wx.FlexGridSizer):

    # noinspection PyShadowingBuiltins,PyUnusedLocal
    def __init__(self, parent, id):
        super().__init__(2, 3, 3)
        self.Add(wx.StaticText(parent, label="Width: "),)
        self.width_control = IntSpin(parent, value="3", min=-1)
        self.Add(self.width_control)
        self.Add(wx.StaticText(parent, label="Height: "),)
        self.height_control = IntSpin(parent, value="3", min=-1)
        self.Add(self.height_control)

    # noinspection PyPep8Naming
    def GetValue(self):
        return self.width_control.GetValue(), self.height_control.GetValue()
