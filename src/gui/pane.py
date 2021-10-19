import typing
import webbrowser
from functools import partial
from typing import Union, List

import numpy as np
import wx
import wx.dataview

from controls import ControlWrapper
from functions import Function, ParamType

if typing.TYPE_CHECKING:
    from datatypes.base import ParamsInstance
    from functions import ParameterTemplate, Function
from gui.basegui import FunctionPaneBase

EVENTS = [
    wx.EVT_BUTTON,
    wx.EVT_SLIDER,
    wx.EVT_CHECKBOX,
    wx.EVT_COMBOBOX,
    wx.EVT_FILEPICKER_CHANGED,
    wx.EVT_TEXT,
    wx.EVT_SPINCTRL,
    wx.EVT_CHOICE,
    wx.EVT_RADIOBUTTON,
    wx.EVT_TOGGLEBUTTON
]


# noinspection PyUnusedLocal
class FunctionPane(FunctionPaneBase):
    def __init__(self, nb: wx.Notebook, func: Function):
        from functions import ParameterTemplate
        super().__init__(nb)
        self.func = func
        self.display_controls = [self.results_matrix, self.results_text, self.results_bitmap]
        self.radio_buttons: List[wx.RadioButton] = []
        self.params: "ParamsInstance" = self.add_input_params(self.func.param_template)
        self.function_name.SetLabel(self.func.name)
        self.help_button.Bind(wx.EVT_BUTTON, self.show_function_help)
        for result in self.func.results:
            result.params = self.add_output_params(result.name,
                                                   [ParameterTemplate(*param) for param in result.PARAMS])
            print(result.params)
        for evt in EVENTS:
            self.Bind(evt, self.on_change)

    def get_input_control(self, param: "ParameterTemplate"):
        tp = ParamType.from_name(param.type_name)
        ctrl = ControlWrapper(self.params_pane, tp, param.default)
        ctrl.SetToolTip(param.description)
        return ctrl

    def instantiate_params(self, params: List["ParameterTemplate"]) -> "ParamsInstance":
        return {x.name: self.get_input_control(x) for x in params}

    @staticmethod
    def show_control(control: wx.Window, shown: wx.ShowEvent) -> None:
        control.Show(shown.IsShown())

    def add_param_controls_to_sizer(self, controls: "ParamsInstance", sizer: wx.FlexGridSizer):
        for name, control in controls.items():
            text = wx.StaticText(self.params_pane, wx.ID_ANY, name)
            sizer.Add(text, 0, wx.EXPAND | wx.ALL, 3)
            sizer.Add(control, 1, wx.EXPAND | wx.ALL, 3)
            control.Bind(wx.EVT_SHOW, partial(self.show_control, text))

    def add_input_params(self, params: List["ParameterTemplate"]) -> "ParamsInstance":
        controls = self.instantiate_params(params)
        self.add_param_controls_to_sizer(controls, self.input_param_sizer)
        return controls

    def add_output_params(self, name: str, params: List["ParameterTemplate"]) -> "ParamsInstance":
        button = wx.RadioButton(self.params_pane)
        self.results_sizer.Add(button, 1, wx.EXPAND)
        self.radio_buttons.append(button)
        text_ctrl = wx.TextCtrl(self.params_pane, value=name)
        self.results_sizer.Add(text_ctrl)
        sizer = wx.FlexGridSizer(2, 0, 3)
        controls = self.instantiate_params(params)
        self.add_param_controls_to_sizer(controls, sizer)
        sizer.AddGrowableCol(1)
        self.results_sizer.AddSpacer(0)
        self.results_sizer.Add(sizer, 1, wx.EXPAND)
        return controls

    def set_display(self, results: Union[wx.Bitmap, Exception, str]) -> None:
        for c in self.display_controls:
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

    def on_change(self, event=None):
        try:
            self.call_func()
            index = [btn.GetValue() for btn in self.radio_buttons].index(True)
            print(index)
            results = self.func.get_result(index)
        except Exception as e:
            self.set_display(e)
            raise e
        else:
            self.set_display(results)
        self.Refresh()

    def call_func(self):
        args = {name: ctrl.GetValue() for name, ctrl in self.params.items()}
        self.func.call(args)

    def get_code(self):
        args = {name: ctrl.GetCode() for name, ctrl in self.params.items()}
        return self.func.as_code(args)

    def show_function_help(self, event):
        if self.func.docs.startswith("file:") or self.func.docs.startswith("http"):
            webbrowser.open(self.func.docs)
        else:
            # FIXME?
            wx.MessageBox(self.func.docs)

    def get_vars(self):
        return self.func.get_vars()
