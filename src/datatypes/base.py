from typing import Union, Dict, Tuple, Type, Any, List

import numpy as np
import wx


class BaseParameter:
    pass


class BaseData:
    PARAMS: Dict[str, Tuple[Any, ...]] = {}
    data: Any

    def __init__(self, name: str, sizer: wx.GridSizer):
        self.name = name
        self.sizer = sizer
        self.params: Dict[str, wx.Control] = {}
        for param, (ctrl, *args) in self.PARAMS.items():
            self.add_widget(param, ctrl, args)

    def add_widget(self, name: str, tp: Type[wx.Control], args: List[Any]):
        parent = self.sizer.GetContainingWindow()
        self.sizer.Add(wx.StaticText(parent, wx.ID_ANY, name), 0, wx.ALL | wx.EXPAND, 3)
        ctrl = tp(parent, wx.ID_ANY, *args)
        self.sizer.Add(ctrl, 0, wx.ALL | wx.EXPAND, 3)
        self.params[name] = ctrl

    def display(self) -> Union[wx.Image, np.array, int, float, str]:
        """Return an object representing the best visualisation of this data
        This could be an image, a matrix or just a value"""
        raise NotImplemented

    def serialize(self) -> str:
        """Return a text representation of this object"""
