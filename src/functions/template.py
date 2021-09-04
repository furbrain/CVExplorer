import re
from typing import Dict, Tuple, List

from lxml import html
# noinspection PyUnresolvedReferences
import cv2

from functions import ParameterTemplate
from functions.function import Function


class FunctionTemplate:
    BASE_URL = "file:///usr/share/doc/opencv-doc/opencv4/html/"

    def __init__(self, fragment: html.HtmlElement):
        parameters: Dict[str, Dict[str, html.HtmlElement]] = {}
        function_table = fragment.find("*/table[@class='memname']")
        if function_table is None:
            arg_types = []
            arg_names = []
            retval = None
        else:
            arg_types = function_table.xpath(".//td[@class='paramtype']")
            arg_names = function_table.xpath(".//td[@class='paramname']")
            retval = function_table.find(".//td[@class='memname']/a")
        if retval:
            retval_text = retval.text_content().strip().split(" cv::")[0]
            if retval_text != "void":
                print(retval_text)
            parameters["retval"] = {"tp": retval, "name": html.fromstring("<p>retval</p>"), "desc": None}
        for tp, name in zip(arg_types, arg_names):
            parameters[name.find("em").text] = {"tp": tp, "name": name}
        self.param_descriptions = self.get_parameter_descriptions(fragment)
        for name, desc in self.param_descriptions.items():
            # print(name)
            if name in parameters:
                parameters[name]["desc"] = desc
        # print(parameters.items())
        self.parameter_templates = {name: ParameterTemplate.from_html_fragments(**value)
                                    for name, value in parameters.items()}
        print(self.parameter_templates)
        self.process_signature(fragment)

    def get_outputs(self) -> List[ParameterTemplate]:
        return [self.parameter_templates[name] for name in self.output_vars]

    def get_vars(self) -> List[ParameterTemplate]:
        print(f"input vars{self.input_vars}")
        return [self.parameter_templates[name] for name in self.input_vars]

    def process_signature(self, fragment):
        python_row = fragment.find("*/table[@class='python_language']//tr[2]")
        if python_row is not None:
            signature = python_row.text_content()
            signature = signature.translate({ord('['): None, ord(']'): None})
            match = re.match(r'(?P<output>.*)=(?P<func>.*)\((?P<args>.*)\)', signature)
            results: Dict[str, str] = match.groupdict()
            self.output_vars = [x.strip() for x in results['output'].split(',')]
            self.func = results['func'].replace("cv.", "cv2.").strip()
            self.input_vars = [x.strip() for x in results['args'].split(',') if x.strip() not in self.output_vars]
            self.name = self.func.replace("cv2.", "")
        else:
            self.name = None

    def is_valid(self):
        return self.name and all(x.is_valid() for x in self.parameter_templates.values())

    @staticmethod
    def get_parameter_descriptions(fragment: html.HtmlElement) -> Dict[str, html.HtmlElement]:
        params = fragment.findall(".//table[@class='params']//tr")
        results = {}
        for param in params:
            name, desc = param.findall("./td")
            results[name.text_content().strip()] = desc
        return results

    def create_function(self):
        return Function(self.name, eval(self.func), self.get_vars(), [x.get_output_data() for x in self.get_outputs()])

    @classmethod
    def get_page_tree(cls, url, absolute=False):
        if not absolute:
            url = cls.BASE_URL + url
        return html.parse(url)

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
            if f.is_valid():
                funcs.append(f)
        return title[0].text, funcs
