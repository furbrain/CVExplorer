from typing import Optional, Union

import cv2
import numpy as np
import wx

from . import ParamsInstance
from .base import BaseData


class ArrayDisplayer:
    PARAMS = {}

    @staticmethod
    def can_handle(data: np.ndarray) -> bool:
        raise NotImplementedError

    @staticmethod
    def display(data: np.ndarray, params: ParamsInstance) -> Union[wx.Bitmap, np.ndarray]:
        raise NotImplementedError


class ImageDisplayer(ArrayDisplayer):
    PARAMS = {
        "AutoExpose": (wx.CheckBox, {}),
        "Brightness": (wx.Slider, {'value': 0, "minValue": -100, "maxValue": 100})
    }

    @staticmethod
    def can_handle(data: np.ndarray) -> bool:
        if (len(data.shape) in (2, 3) and
                (data.shape[0] > 10 and data.shape[1] > 10) and
                (len(data.shape) == 2 or data.shape[2] in (1, 3, 4))):
            return True
        else:
            return False

    @staticmethod
    def display(data: np.ndarray, params: ParamsInstance) -> Union[wx.Bitmap, np.ndarray]:
        h, w = data.shape[:2]
        if params["AutoExpose"].GetValue():
            if len(data.shape) == 3 and data.shape[2] >= 3:
                img_yuv = cv2.cvtColor(data, cv2.COLOR_BGR2YUV)
                img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
                result = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
            else:
                result = cv2.equalizeHist(data)
        else:
            b = params["Brightness"].GetValue()
            result = cv2.add(data, (b, b, b, 0))
        if len(data.shape) == 3 and data.shape[2] >= 3:
            result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        else:
            result = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
        bitmap = wx.Bitmap.FromBuffer(w, h, result)
        return bitmap


class MatrixDisplayer(ArrayDisplayer):

    @staticmethod
    def can_handle(data: np.ndarray) -> bool:
        return len(data.shape) <= 2

    @staticmethod
    def display(data: np.ndarray, params: ParamsInstance) -> Union[wx.Bitmap, np.ndarray]:
        return data


class ImageData(BaseData):
    IMAGE_COUNTER = 1

    ARRAYDISPLAYERS = [
        ImageDisplayer,
        MatrixDisplayer
    ]

    # set our params to be all of the params for the various array displayers
    PARAMS = {key: value for displayer in ARRAYDISPLAYERS for key, value in displayer.PARAMS.items()}

    def __init__(self):
        name = f"image{self.IMAGE_COUNTER}"
        ImageData.IMAGE_COUNTER += 1
        super().__init__(name)
        self.data: Optional[np.ndarray] = None
        self.last_displayer: Optional[ArrayDisplayer] = None

    def display(self) -> Union[wx.Bitmap, np.array]:
        for displayer in self.ARRAYDISPLAYERS:
            if displayer.can_handle(self.data):
                if displayer != self.last_displayer:
                    for param in self.params.values():
                        param.Hide()
                    for param_name in displayer.PARAMS:
                        self.params[param_name].Show()
                    self.last_displayer = displayer
                return displayer.display(self.data, self.params)
        else:
            raise ValueError(f"Unknown array format {self.data.shape}")
