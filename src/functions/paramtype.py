from typing import Type, Union, Dict, ClassVar, Any, Protocol, Tuple, Optional, Set

import attr
import wx
from wx.lib.agw.floatspin import FloatSpin

import controls


class ParamControl(Protocol):
    # noinspection PyUnusedLocal,PyShadowingBuiltins
    def __init__(self, parent: wx.Window, id: int):
        ...

    # noinspection PyPep8Naming
    def SetValue(self, value: Any) -> None:
        ...

    # noinspection PyPep8Naming
    def GetValue(self) -> Any:
        ...

    # noinspection PyPep8Naming
    def SetToolTip(self, text: str) -> None:
        ...


@attr.s(auto_attribs=True)
class ParamType:
    # Class level variables
    INITIALISED: ClassVar[bool] = False
    REGISTER: ClassVar[Dict[str, "ParamType"]] = {}
    BUILT_INS: ClassVar[Dict[Union[Type, str], Tuple[ParamControl, Any]]] = {
        int: (controls.IntSpin, "1"),
        float: (FloatSpin, 1.0),
        bool: (wx.CheckBox, False),
        "Size": (controls.SizeControl, None),
        "Point": (controls.PointControl, None),
        "Array": (controls.InputImage, None),
        str: (wx.TextCtrl, "")
    }
    BUILT_IN_MAPS: ClassVar[Dict[str, str]] = {
        "double": "float",
        "OutputArray": "Array",
        "InputArray": "Array",
        "Mat": "Array",
        "String": "str"
    }
    MISSING_TYPES: ClassVar[Set[str]] = set()
    # instance variables
    name: str
    type: Union[str, Type]
    input_ctrl: Type[ParamControl]
    default: Any = None

    def __attrs_post_init__(self):
        self.REGISTER[self.name] = self

    @classmethod
    def from_name(cls, name: Union[str, Type]) -> Optional["ParamType"]:
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

    def get_input_control(self, parent: wx.Window, default=None) -> ParamControl:
        ctrl = self.create_control(parent)
        if default is not None:
            ctrl.SetValue(default)
        else:
            print("Type default", repr(self.default), repr(ctrl))
            ctrl.SetValue(self.default)
        return ctrl

    def create_control(self, parent):
        return self.input_ctrl(parent, id=wx.ID_ANY)

    def get_output_data(self, name: str):
        from datatypes import OutputData
        return OutputData.from_type(self.type, name)

    @classmethod
    def initialise(cls):
        if not cls.INITIALISED:
            for tp, (ctrl, default) in cls.BUILT_INS.items():
                if isinstance(tp, str):
                    cls(tp, tp, ctrl, default)
                else:
                    cls(tp.__name__, tp, ctrl, default)
            for name, target in cls.BUILT_IN_MAPS.items():
                cls.REGISTER[name] = cls.REGISTER[target]
            cls.INITIALISED = True
