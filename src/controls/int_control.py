import wx


class IntSpin(wx.SpinCtrl):

    def GetValue(self):
        return int(super().GetValue())
