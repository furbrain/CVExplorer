import typing
from typing import Union, Type, Any, ClassVar, List, Optional
from controls import ParamsInstance

import numpy as np
import wx

from .image import ImageDisplayer, MatrixDisplayer, ArrayDisplayer

if typing.TYPE_CHECKING:
    from functions import ParameterTemplate


class BaseParameter:
    pass


class OutputData:
    ARRAYDISPLAYERS = [
        ImageDisplayer,
        MatrixDisplayer
    ]
    PARAMS = [p for displayer in ARRAYDISPLAYERS for p in displayer.PARAMS]
    data: Any

    def __init__(self, name: str):
        self.data: Optional[np.ndarray] = None
        self.last_displayer: Optional[ArrayDisplayer] = None
        self.name = name
        self.params: ParamsInstance = {}

    def display(self) -> Union[wx.Bitmap, np.ndarray, str]:
        """Return an object representing the best visualisation of this data
        This could be an image, a matrix or just a value"""
        for displayer in self.ARRAYDISPLAYERS:
            if displayer.can_handle(self.data):
                if displayer != self.last_displayer:
                    for param in self.params.values():
                        param.Hide()
                    for param_name in displayer.PARAMS:
                        self.params[param_name.name].Show()
                    self.last_displayer = displayer
                return displayer.display(self.data, self.params)
        else:
            raise ValueError(f"Unknown array format {self.data.shape}")
