from typing import Union, Dict, Tuple, Type, Any, List

import numpy as np
import wx


class BaseParameter:
    pass


ParamsTemplate = Dict[str, Tuple[Type[wx.Control], Tuple]]
ParamsInstance = Dict[str, wx.Control]


class BaseData:
    PARAMS: ParamsTemplate = {}
    data: Any

    def __init__(self, name: str):
        self.name = name
        self.params: ParamsInstance = {}

    def display(self) -> Union[wx.Image, np.array, int, float, str]:
        """Return an object representing the best visualisation of this data
        This could be an image, a matrix or just a value"""
        raise NotImplemented

    def serialize(self) -> str:
        """Return a text representation of this object"""
