import wx


class FunctionPane(wx.Panel):
    def __init__(self, nb: wx.Notebook):
        super().__init__(nb)
        self.display = None
        self.display_pane = wx.ScrolledWindow(self, style=wx.TAB_TRAVERSAL)
        self.params_pane = wx.ScrolledWindow(self, style=wx.TAB_TRAVERSAL)
        self.params_pane.SetMinSize((200, -1))
        self.display_pane.SetScrollRate(10, 10)
        self.params_pane.SetScrollRate(10, 10)

        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)  # top level
        sizer_2 = wx.BoxSizer(wx.VERTICAL)  # for the params bit
        sizer_3 = wx.BoxSizer(wx.VERTICAL)  # just to hold the bitmappy jobby
        self.bitmap = wx.StaticBitmap(self.display_pane)
        sizer_1.Add(self.display_pane, 1, wx.ALL | wx.EXPAND, 3)
        sizer_1.Add(wx.StaticLine(self, style=wx.LI_VERTICAL))
        sizer_1.Add(self.params_pane, 0, wx.ALL | wx.EXPAND, 3)
        self.param_sizer = wx.FlexGridSizer(2, 0, 0)
        sizer_2.Add(self.param_sizer, 1, wx.ALL | wx.EXPAND, 3)
        sizer_2.Add(wx.StaticLine(self, style=wx.LI_HORIZONTAL))
        sizer_3.Add(self.bitmap, 0)
        self.SetSizer(sizer_1)
        self.display_pane.SetSizer(sizer_3)
        self.params_pane.SetSizer(sizer_2)

    def get_results_sizer(self):
        sizer = wx.FlexGridSizer(2, 0, 0)
        self.params_pane.GetSizer().Add(sizer, 1, wx.ALL | wx.EXPAND, 3)
        return sizer

    def set_display(self, results):
        if isinstance(results, wx.Bitmap):
            self.bitmap.SetVirtualSize(results.GetSize())
            self.bitmap.SetBitmap(results)
            self.bitmap.Refresh()
