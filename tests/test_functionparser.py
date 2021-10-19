from unittest import TestCase

from lxml import html

from parser.functionparser import FunctionParser
import os.path

FIXTURES_FILTER_HTML = "/usr/share/doc/opencv-doc/opencv4/html/d4/d86/group__imgproc__filter.html"
FIXTURES_FRAGMENT_HTML = os.path.join(os.path.dirname(__file__), "fixtures/filter_fragment.html")


class TestFunctionParser(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with open(FIXTURES_FRAGMENT_HTML) as f:
            cls.pyrDown_element = f.read()

    def setUp(self) -> None:
        self.function_parser = FunctionParser(html.fromstring(self.pyrDown_element, base_url=FIXTURES_FILTER_HTML),
                                              url=FIXTURES_FILTER_HTML)

    def test_parse_signature_simple(self):
        test = "result = cv.function(a)"
        results = ("function", ["a"], ["result"])
        self.assertTupleEqual(results, FunctionParser.parse_signature(test))

    def test_parse_signature_multiple_results(self):
        test = "result, result2 = cv.function(a)"
        results = ("function", ["a"], ["result", "result2"])
        self.assertTupleEqual(results, FunctionParser.parse_signature(test))

    def test_parse_signature_multiple_args(self):
        test = "result = cv.function(a, b)"
        results = ("function", ["a", "b"], ["result"])
        self.assertTupleEqual(results, FunctionParser.parse_signature(test))

    def test_parse_signature_keyword_args(self):
        test = "result = cv.function(a, [b, [c]])"
        results = ("function", ["a", "b", "c"], ["result"])
        self.assertTupleEqual(results, FunctionParser.parse_signature(test))

    def test_get_signature(self):
        results = ("pyrDown", ["src", "dstsize", "borderType"], ["dst"])
        self.assertTupleEqual(results, self.function_parser.get_signature())

    def test_get_type_element(self):
        result = self.function_parser.get_type_element("src")
        self.assertEqual("InputArray", result.text_content().strip())

    def test_get_default_element(self):
        result = self.function_parser.get_default_element("dstsize")
        self.assertEqual("dstsize = Size(),", result.text_content().strip())

    def test_get_description_element(self):
        result = self.function_parser.get_description_element("dstsize")
        self.assertEqual("size of the output image.", result.text_content().strip())

    def test_get_type_from_elements(self):
        for arg, expected in [
                    ("dst", "OutputArray"),
                    ("src", "InputArray"),
                    ("dstsize", "Size"),
                    ("borderType", "BorderTypes")]:
            with self.subTest(f"Checking type for {arg}"):
                tp = self.function_parser.get_type_element(arg)
                name = self.function_parser.get_default_element(arg)
                self.assertEqual(expected, self.function_parser.get_type_from_elements(tp, name))
