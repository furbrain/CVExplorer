from typing import List

import attr
# noinspection PyUnresolvedReferences
import cv2

from .function import Function
from .parameter import ParameterTemplate


@attr.s(auto_attribs=True)
class FunctionTemplate:
    name: str
    inputs: List[ParameterTemplate]
    outputs: List[ParameterTemplate]

    def create_function(self):
        return Function(self.name,
                        eval(f"cv2.{self.name}"),
                        self.inputs,
                        [x.get_output_data() for x in self.outputs])
