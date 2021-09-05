from functools import partial
from typing import Callable, Optional, Union, List

import numpy as np
import wx
import wx.dataview

from datatypes.base import ParamsInstance
from functions import ParameterTemplate
from gui.basegui import FunctionPaneBase

EVENTS = [
    wx.EVT_BUTTON,
    wx.EVT_SLIDER,
    wx.EVT_CHECKBOX,
    wx.EVT_COMBOBOX,
    wx.EVT_FILEPICKER_CHANGED,
    wx.EVT_TEXT,
    wx.EVT_SPINCTRL,
    wx.EVT_CHOICE
]


# noinspection PyUnusedLocal
class FunctionPane(FunctionPaneBase):
    def __init__(self, nb: wx.Notebook):
        super().__init__(nb)
        self.change_handler: Optional[Callable] = None
        self.results_controls = [self.results_matrix, self.results_text, self.results_bitmap]
        for evt in EVENTS:
            self.Bind(evt, self.on_change)
        for c in self.results_controls:
            c.Hide()

    def instantiate_params(self, params: List[ParameterTemplate]) -> ParamsInstance:
        return {x.name: x.get_input_control(self.params_pane) for x in params}

    @staticmethod
    def show_control(control: wx.Window, shown: wx.ShowEvent) -> None:
        control.Show(shown.IsShown())

    def add_param_controls_to_sizer(self, controls: ParamsInstance, sizer: wx.FlexGridSizer):
        for name, control in controls.items():
            text = wx.StaticText(self.params_pane, wx.ID_ANY, name)
            sizer.Add(text, 0, wx.EXPAND | wx.ALL, 3)
            sizer.Add(control, 1, wx.EXPAND | wx.ALL, 3)
            control.Bind(wx.EVT_SHOW, partial(self.show_control, text))

    def add_input_params(self, params: List[ParameterTemplate]) -> ParamsInstance:
        controls = self.instantiate_params(params)
        self.add_param_controls_to_sizer(controls, self.input_param_sizer)
        return controls

    def add_output_params(self, name: str, params: List[ParameterTemplate]) -> ParamsInstance:
        sizer = wx.FlexGridSizer(2, 0, 3)
        controls = self.instantiate_params(params)
        self.add_param_controls_to_sizer(controls, sizer)
        sizer.AddGrowableCol(1)
        box = wx.StaticBoxSizer(wx.VERTICAL, self.params_pane, label=name)
        box.Add(sizer, 1, wx.EXPAND)
        self.params_sizer.Add(box, 1, wx.EXPAND)
        return controls

    def set_display(self, results: Union[wx.Bitmap, Exception, str]) -> None:
        for c in self.results_controls:
            c.Hide()
        if isinstance(results, wx.Bitmap):
            self.results_bitmap.SetVirtualSize(results.GetSize())
            self.results_bitmap.SetBitmap(results)
            self.results_bitmap.Show()
        elif isinstance(results, (Exception, str)):
            self.results_text.ChangeValue(f"Error: {results}")
            self.results_text.Show()
        elif isinstance(results, np.ndarray):
            self.results_matrix.DeleteAllItems()
            self.results_matrix.ClearColumns()
            for i in range(results.shape[1]):
                self.results_matrix.AppendTextColumn(str(i))
            for i in range(results.shape[0]):
                self.results_matrix.AppendItem([str(x) for x in results[i, :]])
            self.results_matrix.Show()
        else:
            self.results_text.ChangeValue(f"Unknown display type: {type(results)}")
        self.display_pane.Layout()
        self.Refresh()
        self.Layout()

    def register_change_handler(self, func: Callable):
        self.change_handler = func

    def on_change(self, event):
        if self.change_handler:
            self.change_handler()
