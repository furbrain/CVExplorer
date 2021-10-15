from typing import ClassVar, Dict, Any, TYPE_CHECKING

import wx

from .array_control import ArrayControl
from .control_type import ParamControl
from .enum_control import EnumControl
from .point_control import PointControl
from .scalar_control import ScalarControl
from .size_control import SizeControl
from .standard_controls import IntControl, FloatControl, BoolControl, TextControl
from .term_criteria_control import TermCriteriaControl

if TYPE_CHECKING:
    from functions import ParamType

BUILT_INS: ClassVar[Dict[str, ParamControl]] = {
    "int": IntControl,
    "float": FloatControl,
    "bool": BoolControl,
    "Size": SizeControl,
    "Point": PointControl,
    "TermCriteria": TermCriteriaControl,
    "Scalar": ScalarControl,
    "Array": ArrayControl,
    "ArrayOfArrays": ArrayControl,
    "str": TextControl
}


def get_control_from_type(parent: wx.Window, tp: "ParamType", default: Any = None) -> "ParamControl":
    from functions import Enum, BuiltInType
    if isinstance(tp, Enum):
        ctrl = EnumControl(parent, wx.ID_ANY, tp)
    elif isinstance(tp, BuiltInType):
        ctrl_type = BUILT_INS[tp.name]
        ctrl = ctrl_type(parent, wx.ID_ANY)
    else:
        raise ValueError("Unknown ParamType")
    if default is not None:
        ctrl.SetValue(default)
    else:
        ctrl.SetValue(tp.default)
    return ctrl
