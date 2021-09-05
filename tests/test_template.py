from unittest import TestCase

import cv2
from lxml import html

from functions.template import FunctionTemplate

FIXTURES_FILTER_HTML = "/usr/share/doc/opencv-doc/opencv4/html/d4/d86/group__imgproc__filter.html"
FIXTURES_FRAGMENT_HTML = "fixtures/filter_fragment.html"


class TestFunctionTemplate(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from functions.paramtype import ParamType
        ParamType.initialise()
        with open(FIXTURES_FILTER_HTML) as f:
            cls.filter_text = f.read()
        with open(FIXTURES_FRAGMENT_HTML) as f:
            cls.filter_fragment = f.read()

    def setUp(self) -> None:
        self.html_frag = html.fromstring(self.filter_fragment)

    def test_create_function(self):
        self.func_template = FunctionTemplate(html.fromstring(self.filter_fragment, base_url=FIXTURES_FILTER_HTML))
        function = self.func_template.create_function()
        self.assertEqual(cv2.pyrDown, function.func)
        self.assertListEqual(["dst1"], [r.name for r in function.results])

    def test_from_url(self):
        _, funcs = FunctionTemplate.from_url("d4/d86/group__imgproc__filter.html")
        from functions import ParamType
        with self.subTest("missing types"):
            self.assertSetEqual(set(), ParamType.MISSING_TYPES)
        with self.subTest("function count"):
            self.assertEqual(22, len(funcs))
