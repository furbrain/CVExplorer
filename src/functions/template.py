from typing import List

import attr
# noinspection PyUnresolvedReferences
import cv2
# noinspection PyUnresolvedReferences
import utils

from .function import Function
from .parameter import ParameterTemplate


@attr.s(auto_attribs=True)
class FunctionTemplate:
    name: str
    module: str
    inputs: List[ParameterTemplate]
    outputs: List[ParameterTemplate]

    def create_function(self):
        return Function(self.name,
                        eval(f"{self.module}.{self.name}"),
                        self.inputs,
                        [x.get_output_data() for x in self.outputs])
