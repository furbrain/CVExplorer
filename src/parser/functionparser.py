import re
from typing import Tuple, List, Dict

from lxml import html

from functions import ParamType, ParameterTemplate
from functions.enum import Enum
from functions.template import FunctionTemplate


class FunctionParser:

    def __init__(self, element: html.HtmlElement):
        self.element: html.HtmlElement = element

    def get_signature(self) -> Tuple[str, List[str], List[str]]:
        python_row = self.element.find("*/table[@class='python_language']//tr[2]")
        if python_row is not None:
            signature = python_row.text_content()
            name, input_vars, output_vars = self.parse_signature(signature)
        else:
            name = None
            input_vars = None
            output_vars = None
        return name, input_vars, output_vars

    @staticmethod
    def parse_signature(signature) -> Tuple[str, List[str], List[str]]:
        # FIXME understand positional vs keyword args...
        signature = signature.translate({ord('['): None, ord(']'): None})
        match = re.match(r'(?P<output>.*)=(?P<func>.*)\((?P<args>.*)\)', signature)
        results: Dict[str, str] = match.groupdict()
        output_vars = [x.strip() for x in results['output'].split(',')]
        name = results['func'].replace("cv.", "").strip()
        input_vars = [x.strip() for x in results['args'].split(',') if x.strip() not in output_vars]
        return name, input_vars, output_vars

    def get_type_element(self, name: str) -> html.HtmlElement:
        return self.element.xpath(f".//td[@class='paramname']//em[text()='{name}']/../../td[@class ='paramtype']")[0]

    def get_default_element(self, name: str) -> html.HtmlElement:
        return self.element.xpath(f".//td[@class='paramname']//em[text()='{name}']/..")[0]

    def get_description_element(self, name: str) -> html.HtmlElement:
        return self.element.xpath(f".//table[@class='params']//td[@class='paramname' and text()='{name}']/../td[2]")[0]

    def get_type(self, name: str) -> ParamType:
        if name == "retval":
            type_name = self.get_retval_typename()
        else:
            tp = self.get_type_element(name)
            name_element = self.get_default_element(name)
            type_name = self.get_type_from_elements(tp, name_element)
        return ParamType.from_name(type_name)

    @staticmethod
    def get_type_from_elements(tp: html.HtmlElement, default: html.HtmlElement) -> str:
        typename = FunctionParser.get_typename_from_element(tp)
        url: html.HtmlElement = default.find(".//a")
        if url is not None:
            url.make_links_absolute(url.base_url)
            href = url.get("href")
            e = Enum.from_url(href)
            if e is not None:
                typename = e.name
        return typename

    @staticmethod
    def get_typename_from_element(tp):
        link = tp.find("a")
        if link is not None:
            typename = link.text.strip()
        else:
            typename = tp.text.strip()
        return typename

    def get_retval_typename(self):
        retval_element = self.element.find(".//table[@class='memname']//td[@class='memname']")
        return self.get_typename_from_element(retval_element)

    def get_description(self, name: str) -> str:
        try:
            result = self.get_description_element(name).text_content()
        except IndexError:
            if name == "retval":
                return ""
            else:
                raise
        return result

    def get_parameter_template(self, name: str) -> ParameterTemplate:
        tp = self.get_type(name)
        desc = self.get_description(name)
        return ParameterTemplate(name, tp, desc)

    def get_function_template(self):
        name, input_vars, output_vars = self.get_signature()
        if name is None:
            return None
        inputs = [self.get_parameter_template(name) for name in input_vars]
        outputs = [self.get_parameter_template(name) for name in output_vars]
        return FunctionTemplate(name, inputs, outputs)
