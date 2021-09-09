from typing import Optional, List, Union

import numpy as np
import wx

from datatypes.image import ImageDisplayer, MatrixDisplayer, ImageData
from functions import ParameterTemplate


class MultiArrayData(ImageData):
    HANDLED_CLASSES = ["ArrayOfArrays"]
    IMAGE_COUNTER = 1

    ARRAYDISPLAYERS = [
        ImageDisplayer,
        MatrixDisplayer
    ]

    # set our params to be all of the params for the various array displayers
    PARAMS = [ParameterTemplate("Index", "int")] + [p for displayer in ARRAYDISPLAYERS for p in displayer.PARAMS]

    def __init__(self, name: str):
        super().__init__(name)
        self.data: Optional[List[np.ndarray]]

    def display(self) -> Union[wx.Bitmap, np.array]:
        index = self.params["Index"].GetValue()
        data = self.data[index]
        for displayer in self.ARRAYDISPLAYERS:
            if displayer.can_handle(data):
                if displayer != self.last_displayer:
                    for param in self.params.values():
                        param.Hide()
                    for param_name in displayer.PARAMS:
                        self.params[param_name.name].Show()
                    self.last_displayer = displayer
                return displayer.display(data, self.params)
        else:
            raise ValueError(f"Unknown array format {self.data.shape}")
