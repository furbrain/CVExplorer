from unittest import TestCase
import os.path
import cv2
from lxml import html

from functions import ParameterTemplate
from functions.template import FunctionTemplate

FIXTURES_FILTER_HTML = "/usr/share/doc/opencv-doc/opencv4/html/d4/d86/group__imgproc__filter.html"
FIXTURES_FRAGMENT_HTML = os.path.join(os.path.dirname(__file__), "fixtures/filter_fragment.html")


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
        self.func_template = FunctionTemplate(
            name="pyrDown",
            module="cv2",
            inputs=[
                ParameterTemplate("src", "InputArray")
            ],
            outputs=[
                ParameterTemplate("dst", "OutputArray")
            ],
            docs="FunctionTemplate docs"
        )
        function = self.func_template.create_function()
        self.assertEqual(cv2.pyrDown, function.func)
        self.assertListEqual(["dst"], [r.name for r in function.results])

