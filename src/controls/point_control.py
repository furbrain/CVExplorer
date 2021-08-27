import wx

from controls import IntSpin


class PointControl(wx.FlexGridSizer):

    # noinspection PyShadowingBuiltins,PyUnusedLocal
    def __init__(self, parent, id):
        super().__init__(2, 3, 3)
        self.Add(wx.StaticText(parent, label="X: "),)
        self.x_control = IntSpin(parent, value="-1", min=-1)
        self.Add(self.x_control)
        self.Add(wx.StaticText(parent, label="Y: "),)
        self.y_control = IntSpin(parent, value="-1", min=-1)
        self.Add(self.y_control)

    # noinspection PyPep8Naming
    def GetValue(self):
        return self.x_control.GetValue(), self.y_control.GetValue()
