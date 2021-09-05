from typing import Any, Optional, ClassVar, Set, Union, Type

import attr
import wx
from lxml import html

from functions.paramtype import ParamType
from functions.enum import Enum


@attr.s(auto_attribs=True)
class ParameterTemplate:
    """This represents a parameter for a function, but is not bound to any controls"""
    MISSING_INPUT_TYPES: ClassVar[Set[str]] = set()
    MISSING_OUTPUT_TYPES: ClassVar[Set[str]] = set()

    name: str
    type: Union[ParamType, str, Type] = attr.ib(converter=ParamType.from_name)
    description: str = ""
    default: Any = None

    def is_valid(self) -> bool:
        return bool(self.name and self.type)

    @classmethod
    def from_html_fragments(cls,
                            name: html.HtmlElement,
                            tp: html.HtmlElement,
                            desc: Optional[html.HtmlElement]) -> "ParameterTemplate":
        link = tp.find("a")
        if link is not None:
            typename = link.text.strip()
        else:
            typename = tp.text.strip()
        var_name = name.find("em").text
        url: html.HtmlElement = name.find(".//a")
        if url is not None:
            print("tracking url")
            url.make_links_absolute(url.base_url)
            href = url.get("href")
            e = Enum.from_url(href)
            if e is not None:
                typename = e.name
        description = desc.text_content().strip()
        param_type = ParamType.from_name(typename)
        return cls(var_name, param_type, description)

    def get_output_data(self):
        return self.type.get_output_data(self.name)

    def get_input_control(self, parent: wx.Window):
        print("default", repr(self.default))
        ctrl = self.type.get_input_control(parent, self.default)
        ctrl.SetToolTip(self.description)
        return ctrl
