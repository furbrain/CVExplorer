from typing import List

import attr

from .template import FunctionTemplate


@attr.s(auto_attribs=True)
class Module:
    name: str
    children: List['Module']
    functions: List[FunctionTemplate]

    def count(self):
        return len(self.functions) + sum(child.count() for child in self.children)
