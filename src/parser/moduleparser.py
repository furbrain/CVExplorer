import re
import urllib.parse
from typing import ClassVar, List

from lxml import html

from functions import Module
from parser import DocumentParser


class ModuleParser:
    BASE_URL: ClassVar[str] = "file:///usr/share/doc/opencv-doc/opencv4/html/"
    MODULE_WHITELIST = [
        "Core",
        "Image Proc",
        "Image file",
        "Camera Cal",
        "2D Features",
        "Object Detection",
        "Computational Photography",
        "ArUco Marker",
        "Optical Flow",
    ]

    def __init__(self):
        self.module_page = html.parse(urllib.parse.urljoin(self.BASE_URL, "modules.html"))
        mods = self.module_page.findall("//table[@class='directory']//tr")
        self.mods_dict = {mod.get('id'): mod for mod in mods}

    def get_modules(self) -> Module:
        return Module("Root", [self.get_module(x) for x in self.get_root_modules()], [])

    def get_module(self, element: html.HtmlElement) -> Module:
        name, functions = DocumentParser(self.get_module_url(element)).get_function_templates()
        submodules = self.get_child_modules(self.get_row_id(element))
        children = [self.get_module(elem) for elem in submodules]
        return Module(name, children, functions)

    def get_child_modules(self, name: str) -> List[html.HtmlElement]:
        template = re.compile(fr"^{name}\d+_$")
        return [element for name, element in self.mods_dict.items() if re.match(template, name)]

    def get_root_modules(self) -> List[html.HtmlElement]:
        root_mods = self.get_child_modules("row_")
        whitelisted = []
        for element in root_mods:
            text: str = self.get_module_name(element)
            if any(text.startswith(x) for x in self.MODULE_WHITELIST):
                whitelisted.append(element)
        return whitelisted

    @staticmethod
    def get_module_name(element) -> str:
        return element.find(".//a[@class='el']").text_content()

    @staticmethod
    def get_module_url(element) -> str:
        return element.find(".//a[@class='el']").get('href')

    @staticmethod
    def get_row_id(element) -> str:
        return element.get('id')
