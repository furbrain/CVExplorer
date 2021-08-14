from typing import Optional

import cv2
import numpy as np
import wx

from .base import BaseData


class ImageData(BaseData):
    PARAMS = {
        "AutoExpose": (wx.CheckBox, ()),
        "Brightness": (wx.Slider, (0, -100, 100))
    }

    def __init__(self, name: str):
        super().__init__(name)
        self.data: Optional[np.array] = None

    def display(self) -> Optional[wx.Bitmap]:
        h, w = self.data.shape[:2]
        if len(self.data.shape) == 3 and self.data.shape[2] >= 3:
            data = cv2.cvtColor(self.data, cv2.COLOR_BGR2RGB)
        else:
            data = cv2.cvtColor(self.data, cv2.COLOR_GRAY2RGB)
        bitmap = wx.Bitmap.FromBuffer(w, h, data)
        return bitmap
