import json
from typing import List, IO

import attr
from cattr.preconf.json import make_converter

from .template import FunctionTemplate


@attr.s(auto_attribs=True)
class Module:
    name: str
    children: List['Module']
    functions: List[FunctionTemplate]

    def count(self):
        return len(self.functions) + sum(child.count() for child in self.children)

    def save(self, f: IO):
        attr.resolve_types(Module)
        converter = make_converter()
        raw_dict = converter.unstructure(self)
        json.dump(raw_dict, f, indent=2)

    @classmethod
    def load(cls, f: IO) -> 'Module':
        attr.resolve_types(Module)
        converter = make_converter()
        raw_dict = json.load(f)
        mod = converter.structure(raw_dict, cls)
        return mod
