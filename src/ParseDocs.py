import json
from pprint import pprint

from parser import DocumentParser
from cattr.preconf.json import make_converter

MODULE_ROOT = "/usr/share/doc/opencv-doc/opencv4/html/modules.html"
IMG_PROC = "/usr/share/doc/opencv-doc/opencv4/html/d4/d86/group__imgproc__filter.html"
results = DocumentParser(IMG_PROC, absolute=True).get_function_templates()
converter = make_converter()
data = converter.unstructure(results)
pprint(data)
print(json.dumps(data, indent=4))
