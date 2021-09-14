from typing import List, Tuple, ClassVar

from lxml import html

from .functionparser import FunctionParser
from functions import FunctionTemplate


class DocumentParser:
    BASE_URL: ClassVar[str] = "file:///usr/share/doc/opencv-doc/opencv4/html/"

    def __init__(self, url: str, absolute=False):
        if not absolute:
            url = self.BASE_URL + url
        self.tree = html.parse(url)

    def get_function_templates(self) -> Tuple[str, List[FunctionTemplate]]:
        title = self.tree.xpath("//div[@class='title']")
        funcs: List[FunctionTemplate] = []
        func_table = self.tree.xpath(
            "//a[@name='func-members']/ancestor::table/descendant::tr[starts-with(@class,'memitem')]")
        for tr in func_table:
            guid = tr.get('class').replace("memitem:", "")
            func_definition = self.tree.xpath(f"//a[@id='{guid}']/following::div")
            f = FunctionParser(func_definition[0]).get_function_template()
            if f is not None:
                funcs.append(f)
        return title[0].text, funcs
