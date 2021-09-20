import json
import re
from typing import Dict, Optional, ClassVar, IO, List

import attr
import cv2
import wx
from cattr.preconf.json import make_converter
from lxml import html

from controls.enum_control import EnumControl
from functions.paramtype import ParamType


@attr.s(auto_attribs=True)
class Enum(ParamType):
    ANCHORS: ClassVar[Dict[str, "Enum"]] = {}
    values: Dict[str, int] = {}
    descriptions: Dict[str, str] = {}

    def create_control(self, parent):
        return EnumControl(parent, wx.ID_ANY, self)

    @staticmethod
    def remove_symbols(text: str):
        return re.sub(r"\W+", "", text)

    @classmethod
    def save(cls, f: IO):
        converter = make_converter()
        attr.resolve_types(cls)
        all_enums = [x for x in cls.REGISTER.values() if isinstance(x, cls)]
        raw_list = converter.unstructure(all_enums)
        json.dump(raw_list, f, indent=2)

    @classmethod
    def load(cls, f: IO):
        converter = make_converter()
        attr.resolve_types(cls)
        raw_list = json.load(f)
        converter.structure(raw_list, List[cls])

    @classmethod
    def from_url(cls, url: str) -> Optional["Enum"]:
        try:
            path, anchor = url.split("#")
            if anchor in cls.ANCHORS:
                return cls.ANCHORS[anchor]
            tree = html.parse(path)
            enum_div = tree.xpath(f"//a[@id='{anchor}']/ancestor::div[@class='memitem']")[0]
            title = enum_div.xpath("preceding::h2")[-1]
            title_text = cls.remove_symbols(title.text_content())
            if title_text in cls.REGISTER:
                return cls.REGISTER[title_text]
            value_rows = enum_div.findall(".//table[@class='fieldtable']//tr")
        except (IndexError, ValueError):
            return None
        values = {}
        descriptions = {}
        default = None
        for row in value_rows:
            try:
                name_element = row.find("./td[@class='fieldname']/div[@class='python_language']")
                match = re.search(r"cv.(\w+)", name_element.text)
                name = match.group(1)
                desc = row.find("./td[@class='fielddoc']").text_content()
                value = getattr(cv2, name)
            except AttributeError:
                pass
            else:
                values[name] = value
                descriptions[name] = desc
                if "DEFAULT" in name.upper():
                    default = name
        if values and descriptions:
            enum = cls(title_text, default=default, values=values, descriptions=descriptions)
            cls.ANCHORS[anchor] = enum
            return enum
        else:
            return None
