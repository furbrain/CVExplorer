import re
from typing import Dict, List, Tuple

# noinspection PyUnresolvedReferences
import cv2
import wx.lib.agw.floatspin
from lxml import html

import datatypes
from controls import InputImage, IntSpin, PointControl, SizeControl
from datatypes import ParamsTemplate
from .enum import Enum
from .function import Function

INPUT_MAPPING = {
    "InputArray": InputImage,
    "float": wx.lib.agw.floatspin.FloatSpin,
    "double": wx.lib.agw.floatspin.FloatSpin,
    "bool": wx.CheckBox,
    "int": IntSpin,
    "Size": SizeControl,
    "Point": PointControl,

}

OUTPUT_MAPPING = {
    "OutputArray": datatypes.ImageData,
    "Mat": datatypes.ImageData,
}


class FunctionTemplate:
    BASE_URL = "file:///usr/share/doc/opencv-doc/opencv4/html/"
    MISSING_INPUT_TYPES = set()
    MISSING_OUTPUT_TYPES = set()

    def __init__(self, fragment: html.HtmlElement):
        type_dict: Dict[str, str] = {}
        function_table = fragment.xpath("*/table[@class='memname']")
        self.valid = False
        if not function_table:
            return
        arg_types = function_table[0].xpath(".//td[@class='paramtype']")
        arg_names = function_table[0].xpath(".//td[@class='paramname']")
        retval = function_table[0].xpath(".//td[@class='memname']/a")
        if retval:
            type_dict['retval'] = retval[0].text
        for tp, name in zip(arg_types, arg_names):
            type_name, var_name = self.get_arg_name_and_type(tp, name)
            type_dict[var_name] = type_name
        self.param_descriptions = self.get_parameter_descriptions(fragment)
        python_row = fragment.xpath("*/table[@class='python_language']//tr/td")
        if python_row:
            signature = f"  {' '.join(row.text for row in python_row if row.text is not None)}"
            signature = signature.translate({ord('['): None, ord(']'): None})
            match = re.match(r'(?P<output>.*)=(?P<func>.*)\((?P<args>.*)\)', signature)
            if not match:
                return
            else:
                results: Dict[str, str] = match.groupdict()
                output_list = [x.strip() for x in results['output'].split(',')]
                self.outputs = {x: type_dict[x] for x in output_list}
                self.func = results['func'].replace("cv.", "cv2.").strip()
                args_list = [x.strip() for x in results['args'].split(',')]
                self.args = {x: type_dict[x] for x in args_list}
                for x in self.outputs.keys():
                    if x in self.args:
                        del self.args[x]
                self.name = self.func.replace("cv2.", "")
                self.valid = True
                for arg in self.args.values():
                    if arg not in INPUT_MAPPING and not Enum.from_name(arg):
                        self.MISSING_INPUT_TYPES.add(arg)
                        self.valid = False
                for output in self.outputs.values():
                    if output not in OUTPUT_MAPPING:
                        self.MISSING_OUTPUT_TYPES.add(output)
                        self.valid = False

    @staticmethod
    def get_arg_name_and_type(tp: html.HtmlElement, name: html.HtmlElement):
        link = tp.find("a")
        if link is not None:
            typename = link.text.strip()
        else:
            typename = tp.text.strip()
        var_name = name.find("em").text
        url: html.HtmlElement = name.find(".//a")
        if url is not None:
            url.make_links_absolute(url.base_url)
            href = url.get("href")
            e = Enum.from_url(href)
            if e is not None:
                typename = e.name

        return typename, var_name

    def get_parameter_descriptions(self, fragment: html.HtmlElement) -> Dict[str, str]:
        params = fragment.findall(".//table[@class='params']//tr")
        results = {}
        for param in params:
            name, desc = param.findall("./td")
            results[name.text_content().strip()] = desc.text_content().strip()
        print(results)
        return results

    def create_function(self):
        params: ParamsTemplate = {}
        for name, tp in self.args.items():
            params[name] = (self.get_input_param(tp), {"tooltip": self.param_descriptions[name]})
        results = [OUTPUT_MAPPING[tp]() for tp in self.outputs.values()]
        func = Function(self.name, eval(self.func), params, results)
        return func

    @classmethod
    def get_page_tree(cls, url, absolute=False):
        if not absolute:
            url = cls.BASE_URL + url
        return html.parse(url)

    @classmethod
    def get_input_param(cls, tp: str):
        if tp in INPUT_MAPPING:
            return INPUT_MAPPING[tp]
        elif Enum.from_name(tp) is not None:
            return Enum.from_name(tp)
        else:
            return None

    @classmethod
    def from_url(cls, url, absolute=False) -> Tuple[str, List["FunctionTemplate"]]:
        tree = cls.get_page_tree(url, absolute)
        title = tree.xpath("//div[@class='title']")
        funcs: List[FunctionTemplate] = []
        func_table = tree.xpath(
            "//a[@name='func-members']/ancestor::table/descendant::tr[starts-with(@class,'memitem')]")
        for tr in func_table:
            guid = tr.get('class').replace("memitem:", "")
            func_definition = tree.xpath(f"//a[@id='{guid}']/following::div")
            f = FunctionTemplate(func_definition[0])
            if f.valid:
                funcs.append(f)
        return title[0].text, funcs


def get_full_url(url):
    return html.parse(FunctionTemplate.BASE_URL + url)


def parse_modules():
    tree = get_full_url("modules.html")
    modules = tree.xpath("//tr/td/a")
    for module in modules:
        url: str = module.get("href")
        if url.startswith("d"):
            parse_page(url, module.text)


def parse_page(url, name):
    print(f"Parsing {name}")
    tree = get_full_url(url)
    title = tree.xpath("//div[@class='title']")
    print(title[0].text)
    func_table = tree.xpath("//a[@name='func-members']/ancestor::table/descendant::tr[starts-with(@class,'memitem')]")
    for tr in func_table:
        guid = tr.get('class').replace("memitem:", "")
        print(guid)
        func_definition = tree.xpath(f"//a[@id='{guid}']/following::div")
        f = FunctionTemplate(func_definition[0])
        print(f)
