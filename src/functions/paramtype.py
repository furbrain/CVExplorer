from typing import Type, Union, Dict, ClassVar, Any, Optional, Set, List

import attr
import wx

import controls


class ParamTypeError(Exception):
    pass


@attr.s(auto_attribs=True, slots=True)
class ParamType:
    # Class level variables
    INITIALISED: ClassVar[bool] = False
    REGISTER: ClassVar[Dict[str, "ParamType"]] = {}
    MISSING_TYPES: ClassVar[Set[str]] = set()
    IGNORE_TYPE_PARTS: ClassVar[List[str]] = [
        "cv::",
        "const",
        "*",
        "&"
    ]
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
        if isinstance(name, str):
            for item in cls.IGNORE_TYPE_PARTS:
                name = name.replace(item, "")
            name = name.strip()
            words = name.split()
            if len(words) > 1:
                trial = cls.from_name(words[0])
                if trial is not None:
                    return trial
        if isinstance(name, cls):
            return name
        if isinstance(name, type):
            name = name.__name__
        if name in cls.REGISTER:
            return cls.REGISTER[name]
        else:
            print(f"Missing {name}:")
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
