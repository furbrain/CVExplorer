from typing import Union, Dict, Tuple, Type, Any, Protocol

import numpy as np
import wx


class BaseParameter:
    pass


# noinspection PyPep8Naming
class SupportsGetValue(Protocol):
    def GetValue(self) -> Any:
        ...

    def Command(self, event: wx.CommandEvent) -> None:
        pass


Control = Union[wx.Control, SupportsGetValue]

ParamsTemplate = Dict[str, Tuple[Type[Control], Dict[str, Any]]]
ParamsInstance = Dict[str, Control]


class BaseData:
    PARAMS: ParamsTemplate = {}
    data: Any

    def __init__(self, name: str):
        self.name = name
        self.params: ParamsInstance = {}

    def display(self) -> Union[wx.Bitmap, np.ndarray, str]:
        """Return an object representing the best visualisation of this data
        This could be an image, a matrix or just a value"""
        raise NotImplementedError
