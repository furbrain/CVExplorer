import re
from typing import Dict, List

import wx.lib.agw.floatspin

import datatypes
from datatypes import ParamsTemplate
from .function import Function
from controls import InputImage, IntSpin
from lxml import html
import cv2


INPUT_MAPPING = {
    "InputArray": InputImage,
    "float": wx.lib.agw.floatspin.FloatSpin,
    "double": wx.lib.agw.floatspin.FloatSpin,
    "int": IntSpin
}

OUTPUT_MAPPING = {
    "OutputArray": datatypes.ImageData
}


class FunctionTemplate:
    def __init__(self, fragment: html.HtmlElement):
        type_dict: Dict[str, str] = {}
        function_table = fragment.xpath("*/table[@class='memname']")
        self.valid = False
        if not function_table:
            return
        arg_types = function_table[0].xpath("*/td[@class='paramtype']")
        arg_names = function_table[0].xpath("*/td[@class='paramname']")
        retval = function_table[0].xpath("*/td[@class='memname']/a")
        if retval:
            type_dict['retval'] = retval[0].text
        for tp, name in zip(arg_types, arg_names):
            type_name, var_name = self.get_arg_name_and_type(tp, name)
            type_dict[var_name] = type_name
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
                print(self.outputs, self.func, self.args)
                self.name = self.func.replace("cv2.", "")
                if all(x in INPUT_MAPPING for x in self.args.values()):
                    if all(x in OUTPUT_MAPPING for x in self.outputs.values()):
                        self.valid = True

    @staticmethod
    def get_arg_name_and_type(tp: html.HtmlElement, name: html.HtmlElement):
        link = tp.find("a")
        if link is not None:
            typename = link.text.strip()
        else:
            typename = tp.text.strip()
        var_name = name.find("em").text
        return typename, var_name

    def create_function(self):
        params: ParamsTemplate = {name: (INPUT_MAPPING[tp], {}) for name, tp in self.args.items()}
        results = [OUTPUT_MAPPING[tp]() for tp in self.outputs.values()]
        func = Function(self.name, eval(self.func), params, results)
        return func

    @staticmethod
    def get_page_tree(url):
        return html.parse(url)

    @classmethod
    def from_url(cls, url) -> List["FunctionTemplate"]:
        tree = cls.get_page_tree(url)
        title = tree.xpath("//div[@class='title']")
        print(title[0].text)
        funcs: List[FunctionTemplate] = []
        func_table = tree.xpath(
            "//a[@name='func-members']/ancestor::table/descendant::tr[starts-with(@class,'memitem')]")
        for tr in func_table:
            guid = tr.get('class').replace("memitem:", "")
            print(guid)
            func_definition = tree.xpath(f"//a[@id='{guid}']/following::div")
            f = FunctionTemplate(func_definition[0])
            if f.valid:
                funcs.append(f)
        return funcs


base_url = "file:///usr/share/doc/opencv-doc/opencv4/html/"


def get_page_tree(url):
    return html.parse(base_url + url)


def parse_modules():
    tree = get_page_tree("modules.html")
    modules = tree.xpath("//tr/td/a")
    for module in modules:
        url: str = module.get("href")
        if url.startswith("d"):
            parse_page(url, module.text)


def parse_page(url, name):
    tree = get_page_tree(url)
    title = tree.xpath("//div[@class='title']")
    print(title[0].text)
    func_table = tree.xpath("//a[@name='func-members']/ancestor::table/descendant::tr[starts-with(@class,'memitem')]")
    for tr in func_table:
        guid = tr.get('class').replace("memitem:", "")
        print(guid)
        func_definition = tree.xpath(f"//a[@id='{guid}']/following::div")
        f = FunctionTemplate(func_definition[0])