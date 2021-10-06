from typing import List, ClassVar

import attr
# noinspection PyUnresolvedReferences
import cv2
# noinspection PyUnresolvedReferences
import utils
from datatypes import OutputData

from .function import Function
from .parameter import ParameterTemplate


@attr.s(auto_attribs=True)
class FunctionTemplate:
    ALL_TEMPLATES: ClassVar[List["FunctionTemplate"]] = []
    name: str
    module: str
    inputs: List[ParameterTemplate]
    outputs: List[ParameterTemplate]
    docs: str

    def __attrs_post_init__(self):
        self.ALL_TEMPLATES.append(self)

    def create_function(self):
        return Function(self.name,
                        eval(f"{self.module}.{self.name}"),
                        self.inputs,
                        [OutputData(x.name) for x in self.outputs],
                        self.docs)

    @classmethod
    def find(cls, text:str) -> List["FunctionTemplate"]:
        return [x for x in cls.ALL_TEMPLATES if text in x.name]

    @classmethod
    def find_one(cls, text:str) -> "FunctionTemplate":
        candidates = cls.find(text)
        if len(candidates)==0:
            raise ValueError(f"FunctionTemplate instance for {text} not found")
        return candidates[0]
