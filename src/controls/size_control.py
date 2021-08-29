import wx

from controls import IntSpin


class SizeControl(wx.Panel):

    # noinspection PyShadowingBuiltins,PyUnusedLocal
    def __init__(self, parent, id):
        super().__init__(parent, id)
        self.sizer = wx.FlexGridSizer(2, 3, 3)
        self.sizer.Add(wx.StaticText(self, label="Width: "),)
        self.width_control = IntSpin(self, value="3", min=-1)
        self.sizer.Add(self.width_control)
        self.sizer.Add(wx.StaticText(self, label="Height: "),)
        self.height_control = IntSpin(self, value="3", min=-1)
        self.sizer.Add(self.height_control)
        self.SetSizer(self.sizer)

    # noinspection PyPep8Naming
    def GetValue(self):
        return self.width_control.GetValue(), self.height_control.GetValue()
