import re
import wx
from typing import Dict, Optional

import cv2
from html import escape as html_escape
from lxml import html

from controls.enum_control import EnumControl


class Enum:
    ANCHORS: Dict[str, "Enum"] = {}
    NAMES: Dict[str, "Enum"] = {}

    def __init__(self, name: str, values: Dict[str, int], descriptions: Dict[str, str]):
        self.name = name
        self.values = values
        self.descriptions = descriptions

    # noinspection PyShadowingBuiltins
    def __call__(self, parent: wx.Window, id):
        return EnumControl(parent, id, self)

    @staticmethod
    def remove_symbols(text: str):
        return re.sub(r"\W+", "", text)

    @staticmethod
    def inner_html(element: html.HtmlElement):
        foreword = html_escape(element.text or '')
        return foreword + ''.join(html.tostring(x, encoding='unicode') for x in element.iterchildren())

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
            if title_text in cls.NAMES:
                return cls.NAMES[title_text]
            value_rows = enum_div.findall(".//table[@class='fieldtable']//tr")
        except (IndexError, ValueError):
            return None
        values = {}
        descriptions = {}
        for row in value_rows:
            try:
                name_element = row.find("./td[@class='fieldname']/div[@class='python_language']")
                match = re.search(r"cv.(\w+)", name_element.text)
                name = match.group(1)
                desc = cls.inner_html(row.find("./td[@class='fielddoc']"))
                numeric_value = getattr(cv2, name)
            except AttributeError:
                pass
            else:
                values[name] = numeric_value
                descriptions[name] = desc
        if values and descriptions:
            enum = cls(title_text, values, descriptions)
            cls.ANCHORS[anchor] = enum
            cls.NAMES[title_text] = enum
            return enum

    @classmethod
    def from_name(cls, text: str) -> Optional["Enum"]:
        print(f"Checking {text}")
        if text in cls.NAMES:
            print(f"found {text}")
            return cls.NAMES[text]
        else:
            return None
