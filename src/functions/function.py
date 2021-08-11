from typing import Callable, Dict, Tuple, List, Type, Any

import wx

from datatypes.base import BaseData


class Function:
    def __init__(self, name: str, func: Callable, params: Dict[str, Tuple], results: List[BaseData]):
        self.name = name
        self.func = func
        self.param_template = params
        self.results: List[BaseData] = results
        self.params: Dict[str, wx.Control] = {}

    def create_params(self, sizer: wx.FlexGridSizer):
        for param, (ctrl, *args) in self.param_template.items():
            self.add_widget(sizer, param, ctrl, args)

    def add_widget(self, sizer: wx.FlexGridSizer, name: str, tp: Type[wx.Control], args: List[Any]):
        parent = sizer.GetContainingWindow()
        sizer.Add(wx.StaticText(parent, wx.ID_ANY, name))
        ctrl = tp(parent, wx.ID_ANY, *args)
        sizer.Add(ctrl)
        self.params[name] = ctrl

    def call(self):
        args = [ctrl.GetValue() for ctrl in self.params.values()]
        results = self.func(*args)
        if len(self.results) == 1:
            self.results[0].data = results
        elif len(self.results) == len(results):
            for result, temp_result in zip(self.results, results):
                result.data = temp_result
        else:
            raise TypeError("Wrong number of results returned")
