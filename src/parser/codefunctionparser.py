import inspect
import types
from typing import List

import docstring_parser
import typing

from functions import FunctionTemplate, ParameterTemplate


class CodeFunctionParser:
    def __init__(self, function: types.FunctionType):
        self.function = function
        self.sig = inspect.signature(function)
        self.docstring = docstring_parser.parse(function.__doc__)

    def get_return_params(self) -> List[ParameterTemplate]:
        return_type = self.sig.return_annotation
        desc = self.docstring.returns.description
        return_types = typing.get_args(return_type)
        if return_types:
            return [ParameterTemplate(f"retval{x}", tp, desc) for x, tp in enumerate(return_types)]
        else:
            return [ParameterTemplate("retval", return_type, desc)]

    def get_parameter(self, name: str) -> ParameterTemplate:
        param = self.sig.parameters[name]
        desc = [p for p in self.docstring.params if p.arg_name == name][0]
        return ParameterTemplate(name, param.annotation, desc.description)

    def get_template(self) -> FunctionTemplate:
        params = [self.get_parameter(param) for param in self.sig.parameters.keys()]
        retvals = self.get_return_params()
        return FunctionTemplate(self.function.__name__, self.function.__module__, params, retvals)
