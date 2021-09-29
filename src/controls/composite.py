from typing import List, Dict, Type, ClassVar

import wx

from functions import ParameterTemplate
from .wrapper import ControlWrapper
from .control_type import ParamControl


# noinspection PyPep8Naming
class CompositeControl(wx.Panel):
    _FIELDS: ClassVar[List["ParameterTemplate"]] = []

    # noinspection PyShadowingBuiltins
    def __init__(self, parent: wx.Window, id: int = wx.ID_ANY):
        super().__init__(parent, id)
        self.sizer = wx.FlexGridSizer(len(self.FIELDS), 3, 3)
        self.controls: Dict[str, ParamControl] = {}
        for field in self.FIELDS:
            self.sizer.Add(wx.StaticText(self, label=field.name), )
            self.controls[field.name] = ControlWrapper(self, field.get_type())
            self.sizer.Add(self.controls[field.name])
        self.SetSizer(self.sizer)

    def SetValue(self, values):
        if values is None:
            values = tuple(field.default for field in self.FIELDS)
        for value, field in zip(values, self.FIELDS):
            self.controls[field.name].SetValue(value)

    def GetValue(self):
        return tuple(self.controls[field.name].GetValue() for field in self.FIELDS)

    def GetCode(self):
        return f"({', '.join(self.controls[field.name].GetCode() for field in self.FIELDS)})"

    @classmethod
    def from_param_list(cls, name: str, params: List["ParameterTemplate"]) -> Type["CompositeControl"]:
        # noinspection PyTypeChecker
        return type(name, (cls,), {"FIELDS": params})

    @classmethod
    def get_fields(cls) -> List["ParameterTemplate"]:
        raise NotImplementedError

    @property
    def FIELDS(self) -> List["ParameterTemplate"]:
        if not self._FIELDS:
            self._FIELDS = self.get_fields()
        return self._FIELDS
