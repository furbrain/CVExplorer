from typing import Type, Union, Dict, ClassVar, Any, Optional, Set

import attr
import wx

import controls


@attr.s(auto_attribs=True, slots=True)
class ParamType:
    # Class level variables
    INITIALISED: ClassVar[bool] = False
    REGISTER: ClassVar[Dict[str, "ParamType"]] = {}
    MISSING_TYPES: ClassVar[Set[str]] = set()
    # instance variables
    name: str
    type: Union[str, Type]
    default: Any = None

    def __attrs_post_init__(self):
        self.REGISTER[self.name] = self

    @classmethod
    def from_name(cls, name: Union["ParamType", str, Type]) -> Optional["ParamType"]:
        if not cls.INITIALISED:
            cls.initialise()
        if isinstance(name, cls):
            return name
        if isinstance(name, type):
            name = name.__name__
        if name in cls.REGISTER:
            return cls.REGISTER[name]
        else:
            print(f"Missing {name}: {type(name)}")
            cls.MISSING_TYPES.add(name)
            return None

    def get_input_control(self, parent: wx.Window, default=None) -> controls.ParamControl:
        ctrl = self.create_control(parent)
        if default is not None:
            ctrl.SetValue(default)
        else:
            ctrl.SetValue(self.default)
        return ctrl

    def create_control(self, parent):
        raise NotImplementedError

    def get_output_data(self, name: str):
        from datatypes import OutputData
        return OutputData.from_type(self.type, name)

    @classmethod
    def initialise(cls):
        if not cls.INITIALISED:
            from .builtintype import BuiltInType
            BuiltInType.initialise_builtins()
            cls.INITIALISED = True

    @classmethod
    def is_valid(cls, name: str):
        return bool(cls.from_name(name))
