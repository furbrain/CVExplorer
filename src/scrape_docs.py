from typing import Dict, Union, List

from lxml import html
import cv2
import urllib.request
import re

from functions.template import FunctionTemplate

functions = {}
base_url = "file:///usr/share/doc/opencv-doc/opencv4/html/"


def get_page_tree(url):
    return html.parse(base_url + url)



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

def parse_modules():
    tree = get_page_tree("modules.html")
    modules = tree.xpath("//tr/td/a")
    for module in modules:
        url: str = module.get("href")
        if url.startswith("d"):
            parse_page(url, module.text)


parse_page("d4/d86/group__imgproc__filter.html", "img proc")
exit()

version = cv2.__version__
print(f"Getting index for {version}")
with urllib.request.urlopen(url) as page:
    tree = html.parse(page)
    paths = tree.xpath('//ul/li[8]/ul/li/a')
    for path in paths:
        print(path.get('href'))
