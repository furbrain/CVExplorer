from typing import Optional, TYPE_CHECKING

import wx

from .base import BaseData

if TYPE_CHECKING:
    pass


class BooleanData(BaseData):
    PARAMS = {
        "Brightness": (wx.Slider, 0, -100, 100)
    }

    def __init__(self, name: str, sizer: wx.GridSizer):
        super().__init__(name, sizer)
        self.data: Optional[bool] = None

    def display(self) -> bool:
        return self.data
