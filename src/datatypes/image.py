from typing import Optional, Union

import cv2
import numpy as np
import wx

from .base import BaseData


class ImageData(BaseData):
    PARAMS = {
        "AutoExpose": (wx.CheckBox, {}),
        "Brightness": (wx.Slider, {'value': 0, "minValue": -100, "maxValue": 100})
    }

    IMAGE_COUNTER = 1

    def __init__(self):
        name = f"image{self.IMAGE_COUNTER}"
        ImageData.IMAGE_COUNTER += 1
        super().__init__(name)
        self.data: Optional[np.array] = None

    @staticmethod
    def is_image(data: np.array) -> bool:
        if len(data.shape) in (2, 3):
            if data.shape[0] > 10 and data.shape[1] > 10:
                if len(data.shape == 2) or data.shape[2] in (1, 3, 4):
                    return True
        return False

    def display(self) -> Union[wx.Bitmap, np.array]:
        if self.is_image(self.data):
            h, w = self.data.shape[:2]
            if self.params["AutoExpose"].GetValue():
                img_yuv = cv2.cvtColor(self.data, cv2.COLOR_BGR2YUV)
                img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
                data = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
            else:
                b = self.params["Brightness"].GetValue()
                data = cv2.add(self.data, (b, b, b, 0))
            if len(self.data.shape) == 3 and self.data.shape[2] >= 3:
                data = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
            else:
                data = cv2.cvtColor(data, cv2.COLOR_GRAY2RGB)
            bitmap = wx.Bitmap.FromBuffer(w, h, data)
            return bitmap
        else:
            if len(self.data.shape) <= 2:
                return self.data
            else:
                raise ValueError(f"Unknown array format {self.data.shape}")
