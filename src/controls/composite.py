from typing import List, TYPE_CHECKING, Dict, Type, ClassVar

import wx

if TYPE_CHECKING:
    from functions import ParameterTemplate
    from controls import ParamControl


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
            self.controls[field.name] = field.get_input_control(self)
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
    def get_fields(cls):
        raise NotImplementedError

    @property
    def FIELDS(self):
        if not self._FIELDS:
            self._FIELDS = self.get_fields()
        return self._FIELDS
