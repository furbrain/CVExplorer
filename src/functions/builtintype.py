from typing import ClassVar, Dict, Union, Type, Tuple, Any

import attr
import wx

from functions import ParamType
import controls


@attr.s(auto_attribs=True, slots=True)
class BuiltInType(ParamType):
    BUILT_INS: ClassVar[Dict[Union[Type, str], Tuple[controls.ParamControl, Any]]] = {
        int: (controls.IntControl, "1"),
        float: (controls.FloatControl, 1.0),
        bool: (controls.BoolControl, False),
        "Size": (controls.SizeControl, None),
        "Point": (controls.PointControl, None),
        "TermCriteria": (controls.TermCriteriaControl, None),
        "Scalar": (controls.ScalarControl, None),
        "Array": (controls.ArrayControl, None),
        "ArrayOfArrays": (controls.ArrayControl, None),
        str: (controls.TextControl, "")
    }
    BUILT_IN_MAPS: ClassVar[Dict[str, str]] = {
        "double": "float",
        "OutputArray": "Array",
        "InputArray": "Array",
        "InputOutputArray": "Array",
        "SparseMat": "Array",
        "Mat": "Array",
        "UMat": "Array",
        "AsyncArray": "Array",
        "OutputArrayOfArrays": "ArrayOfArrays",
        "String": "str",
        "char": "str",
        "Point2f": "Point",
        "Point2d": "Point",
        "size_t": "int",
        "Size2d": "Size"
    }
    input_ctrl: Type[controls.ParamControl] = None

    def create_control(self, parent):
        return self.input_ctrl(parent, id=wx.ID_ANY)

    @classmethod
    def initialise_builtins(cls):
        for tp, (ctrl, default) in cls.BUILT_INS.items():
            if isinstance(tp, str):
                cls(tp, tp, default, ctrl)
            else:
                cls(tp.__name__, tp, default, ctrl)
        for name, target in cls.BUILT_IN_MAPS.items():
            cls.REGISTER[name] = cls.REGISTER[target]
