from typing import ClassVar, Dict, Union, Type, Any

import attr

from functions import ParamType


@attr.s(auto_attribs=True, slots=True)
class BuiltInType(ParamType):
    DEFAULTS: ClassVar[Dict[Union[Type, str], Any]] = {
        int: "1",
        float: 1.0,
        bool: False,
        "Size": None,
        "Point": None,
        "TermCriteria": None,
        "Scalar": None,
        "Array": None,
        "ArrayOfArrays": None,
        str: ""
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
        "ndarray": "Array",
        "OutputArrayOfArrays": "ArrayOfArrays",
        "String": "str",
        "char": "str",
        "Point2f": "Point",
        "Point2d": "Point",
        "size_t": "int",
        "Size2d": "Size"
    }

    @classmethod
    def initialise_builtins(cls):
        for tp,  default in cls.DEFAULTS.items():
            cls(tp, default)
        for name, target in cls.BUILT_IN_MAPS.items():
            cls.REGISTER[name] = cls.REGISTER[target]
