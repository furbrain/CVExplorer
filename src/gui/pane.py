import wx

from datatypes.base import ParamsTemplate, ParamsInstance


class FunctionPane(wx.Panel):
    def __init__(self, nb: wx.Notebook):
        super().__init__(nb)
        self.display = None
        self.display_pane = wx.ScrolledWindow(self, style=wx.TAB_TRAVERSAL)
        self.params_pane = wx.ScrolledWindow(self, style=wx.TAB_TRAVERSAL)
        self.params_pane.SetMinSize((300, -1))
        self.display_pane.SetScrollRate(10, 10)
        self.params_pane.SetScrollRate(10, 10)

        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)  # top level
        sizer_3 = wx.BoxSizer(wx.VERTICAL)  # just to hold the bitmappy jobby
        self.bitmap = wx.StaticBitmap(self.display_pane)
        sizer_1.Add(self.display_pane, 1, wx.ALL | wx.EXPAND, 3)
        sizer_1.Add(wx.StaticLine(self, style=wx.LI_VERTICAL), 0, wx.ALL | wx.EXPAND, 3)
        sizer_1.Add(self.params_pane, 0, wx.ALL | wx.EXPAND, 3)
        self.input_param_sizer = wx.FlexGridSizer(2, 0, 3)
        self.input_param_sizer.AddGrowableCol(1)
        self.params_sizer = wx.BoxSizer(wx.VERTICAL)
        self.params_sizer.Add(self.input_param_sizer, 1, wx.ALL | wx.EXPAND, 3)
        self.params_sizer.Add(wx.StaticLine(self.params_pane, style=wx.LI_HORIZONTAL), 0, wx.ALL | wx.EXPAND, 3)
        sizer_3.Add(self.bitmap, 0)
        self.SetSizer(sizer_1)
        self.display_pane.SetSizer(sizer_3)
        self.params_pane.SetSizer(self.params_sizer)

    def instantiate_params(self, params: ParamsTemplate) -> ParamsInstance:
        return {name: ctrl(self.params_pane, wx.ID_ANY, *args) for name, (ctrl, args) in params.items()}

    def add_param_controls_to_sizer(self, controls: ParamsInstance, sizer: wx.FlexGridSizer):
        for name, control in controls.items():
            sizer.Add(wx.StaticText(self.params_pane, wx.ID_ANY, name), 0, wx.EXPAND | wx.ALL, 3)
            sizer.Add(control, 1, wx.EXPAND | wx.ALL, 3)

    def add_input_params(self, params: ParamsTemplate) -> ParamsInstance:
        controls = self.instantiate_params(params)
        self.add_param_controls_to_sizer(controls, self.input_param_sizer)
        return controls

    def add_output_params(self, name: str, params: ParamsTemplate) -> ParamsInstance:
        sizer = wx.FlexGridSizer(2,0,3)
        controls = self.instantiate_params(params)
        self.add_param_controls_to_sizer(controls, sizer)
        sizer.AddGrowableCol(1)
        box = wx.StaticBoxSizer(wx.VERTICAL, self.params_pane, label=name)
        box.Add(sizer, 1, wx.EXPAND)
        self.params_sizer.Add(box, 1, wx.EXPAND)
        return controls

    def set_display(self, results):
        if isinstance(results, wx.Bitmap):
            self.bitmap.SetVirtualSize(results.GetSize())
            self.bitmap.SetBitmap(results)
            self.bitmap.Refresh()