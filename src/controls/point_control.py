import wx

from controls import IntSpin


class PointControl(wx.Panel):

    # noinspection PyShadowingBuiltins,PyUnusedLocal
    def __init__(self, parent, id):
        super().__init__(parent, id)
        self.sizer = wx.FlexGridSizer(2, 3, 3)
        self.sizer.Add(wx.StaticText(self, label="X: "),)
        self.x_control = IntSpin(self, value="-1", min=-1)
        self.sizer.Add(self.x_control)
        self.sizer.Add(wx.StaticText(self, label="Y: "),)
        self.y_control = IntSpin(self, value="-1", min=-1)
        self.sizer.Add(self.y_control)
        self.SetSizer(self.sizer)
        self.Layout()

    # noinspection PyPep8Naming
    def GetValue(self):
        return self.x_control.GetValue(), self.y_control.GetValue()
