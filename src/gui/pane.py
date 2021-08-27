from typing import Callable, Optional, Union

import wx
import wx.grid

from datatypes.base import ParamsTemplate, ParamsInstance

EVENTS = [
    wx.EVT_BUTTON,
    wx.EVT_SLIDER,
    wx.EVT_CHECKBOX,
    wx.EVT_COMBOBOX,
    wx.EVT_FILEPICKER_CHANGED,
    wx.EVT_TEXT,
    wx.EVT_SPINCTRL
]


# noinspection PyUnusedLocal
class FunctionPane(wx.Panel):
    def __init__(self, nb: wx.Notebook):
        super().__init__(nb)
        self.display = None
        self.change_handler: Optional[Callable] = None
        self.display_pane = wx.ScrolledWindow(self, style=wx.TAB_TRAVERSAL)
        self.params_pane = wx.ScrolledWindow(self, style=wx.TAB_TRAVERSAL)
        self.params_pane.SetMinSize((300, -1))
        self.display_pane.SetScrollRate(10, 10)
        self.params_pane.SetScrollRate(10, 10)

        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)  # top level
        sizer_3 = wx.BoxSizer(wx.VERTICAL)  # just to hold the bitmap jobby
        self.results_bitmap = wx.StaticBitmap(self.display_pane)
        self.results_text = wx.TextCtrl(self.display_pane, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.results_matrix = wx.grid.Grid()
        self.results_controls = [self.results_matrix, self.results_text, self.results_bitmap]
        sizer_1.Add(self.display_pane, 1, wx.ALL | wx.EXPAND, 3)
        sizer_1.Add(wx.StaticLine(self, style=wx.LI_VERTICAL), 0, wx.ALL | wx.EXPAND, 3)
        sizer_1.Add(self.params_pane, 0, wx.ALL | wx.EXPAND, 3)
        self.input_param_sizer = wx.FlexGridSizer(2, 0, 3)
        self.input_param_sizer.AddGrowableCol(1)
        self.params_sizer = wx.BoxSizer(wx.VERTICAL)
        self.params_sizer.Add(self.input_param_sizer, 1, wx.ALL | wx.EXPAND, 3)
        self.params_sizer.Add(wx.StaticLine(self.params_pane, style=wx.LI_HORIZONTAL), 0, wx.ALL | wx.EXPAND, 3)
        sizer_3.Add(self.results_bitmap, 1, wx.ALL | wx.EXPAND, 3)
        sizer_3.Add(self.results_text, 1, wx.ALL | wx.EXPAND, 3)
        sizer_3.Add(self.results_matrix, 1, wx.ALL | wx.EXPAND, 3)
        self.SetSizer(sizer_1)
        self.display_pane.SetSizer(sizer_3)
        self.params_pane.SetSizer(self.params_sizer)
        for evt in EVENTS:
            self.Bind(evt, self.on_change)
        for c in self.results_controls:
            c.Hide()

    def instantiate_params(self, params: ParamsTemplate) -> ParamsInstance:
        return {name: ctrl(self.params_pane, wx.ID_ANY, **args) for name, (ctrl, args) in params.items()}

    def add_param_controls_to_sizer(self, controls: ParamsInstance, sizer: wx.FlexGridSizer):
        for name, control in controls.items():
            sizer.Add(wx.StaticText(self.params_pane, wx.ID_ANY, name), 0, wx.EXPAND | wx.ALL, 3)
            sizer.Add(control, 1, wx.EXPAND | wx.ALL, 3)

    def add_input_params(self, params: ParamsTemplate) -> ParamsInstance:
        controls = self.instantiate_params(params)
        self.add_param_controls_to_sizer(controls, self.input_param_sizer)
        return controls

    def add_output_params(self, name: str, params: ParamsTemplate) -> ParamsInstance:
        sizer = wx.FlexGridSizer(2, 0, 3)
        controls = self.instantiate_params(params)
        self.add_param_controls_to_sizer(controls, sizer)
        sizer.AddGrowableCol(1)
        box = wx.StaticBoxSizer(wx.VERTICAL, self.params_pane, label=name)
        box.Add(sizer, 1, wx.EXPAND)
        self.params_sizer.Add(box, 1, wx.EXPAND)
        return controls

    def set_display(self, results: Union[wx.Bitmap, Exception]) -> None:
        for c in self.results_controls:
            c.Hide()
        if isinstance(results, wx.Bitmap):
            self.results_bitmap.SetVirtualSize(results.GetSize())
            self.results_bitmap.SetBitmap(results)
            self.results_bitmap.Show()
            self.results_bitmap.Refresh()
        elif isinstance(results, Exception):
            self.results_text.ChangeValue(f"Error: {results}")
            self.results_text.Show()

    def register_change_handler(self, func: Callable):
        self.change_handler = func

    def on_change(self, event):
        if self.change_handler:
            self.change_handler()
