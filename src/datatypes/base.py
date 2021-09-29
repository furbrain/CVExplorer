import typing
from typing import Union, Type, Any, ClassVar, List
from controls import ParamsInstance

import numpy as np
import wx

if typing.TYPE_CHECKING:
    from functions import ParameterTemplate


class BaseParameter:
    pass


class OutputData:
    HANDLED_CLASSES: ClassVar[List[Union[Type, str]]] = []
    PARAMS: ClassVar[List["ParameterTemplate"]] = []
    data: Any

    def __init__(self, name: str):
        self.name = name
        self.params: ParamsInstance = {}

    def display(self) -> Union[wx.Bitmap, np.ndarray, str]:
        """Return an object representing the best visualisation of this data
        This could be an image, a matrix or just a value"""
        raise NotImplementedError

    @classmethod
    def handles_type(cls, tp: Union[Type, str]) -> bool:
        return tp in cls.HANDLED_CLASSES

    @classmethod
    def from_type(cls, tp: Union[Type, str], name: str) -> "OutputData":
        for klass in cls.__subclasses__():
            if klass.handles_type(tp):
                return klass(name)
