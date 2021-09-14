from typing import Any

import attr
import wx

from functions.paramtype import ParamType, ParamTypeError


@attr.s(auto_attribs=True)
class ParameterTemplate:
    """This represents a parameter for a function, but is not bound to any controls"""
    name: str
    type_name: str = attr.ib()
    description: str = ""
    default: Any = None

    # noinspection PyUnusedLocal,PyUnresolvedReferences
    @type_name.validator
    def check_type(self, attribute, value):
        if not ParamType.is_valid(value):
            raise ParamTypeError(f"Unknown Param Type: {value}")

    def is_valid(self) -> bool:
        return bool(self.name and self.type_name)

    def get_output_data(self):
        return ParamType.from_name(self.type_name).get_output_data(self.name)

    def get_input_control(self, parent: wx.Window):
        ctrl = ParamType.from_name(self.type_name).get_input_control(parent, self.default)
        ctrl.SetToolTip(self.description)
        return ctrl
