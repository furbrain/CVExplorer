from typing import Any, Union, Type

import attr
import wx

from functions.paramtype import ParamType


@attr.s(auto_attribs=True)
class ParameterTemplate:
    """This represents a parameter for a function, but is not bound to any controls"""
    name: str
    type: Union[ParamType, str, Type] = attr.ib(converter=ParamType.from_name)
    description: str = ""
    default: Any = None

    def is_valid(self) -> bool:
        return bool(self.name and self.type)

    def get_output_data(self):
        return self.type.get_output_data(self.name)

    def get_input_control(self, parent: wx.Window):
        ctrl = self.type.get_input_control(parent, self.default)
        ctrl.SetToolTip(self.description)
        return ctrl
