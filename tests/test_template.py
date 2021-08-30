from unittest import TestCase

import cv2
from lxml import html
from functions.template import FunctionTemplate

FIXTURES_FILTER_HTML = "/usr/share/doc/opencv-doc/opencv4/html/d4/d86/group__imgproc__filter.html"
FIXTURES_FRAGMENT_HTML = "fixtures/filter_fragment.html"


class TestFunctionTemplate(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with open(FIXTURES_FILTER_HTML) as f:
            cls.filter_text = f.read()
        with open(FIXTURES_FRAGMENT_HTML) as f:
            cls.filter_fragment = f.read()

    def setUp(self) -> None:
        self.html_frag = html.fromstring(self.filter_fragment)

    def test_get_arg_name_and_type_linked(self):
        html_type = """
          <td class="paramtype">
            <a class="el" href="../../dc/d84/group__core__basic.html">OutputArray</a>
            &nbsp;
          </td>"""
        html_name = """<td class="paramname"><em>dst</em>, </td>"""
        typename, varname = FunctionTemplate.get_arg_name_and_type(html.fromstring(html_type),
                                                                   html.fromstring(html_name))
        self.assertEqual("OutputArray", typename)
        self.assertEqual("dst", varname)

    def test_get_arg_name_and_type_unlinked(self):
        html_type = """<td class="paramtype">int&nbsp;</td>"""
        html_name = """<td class="paramname"><em>ddepth</em>, </td>"""
        typename, varname = FunctionTemplate.get_arg_name_and_type(html.fromstring(html_type),
                                                                   html.fromstring(html_name))
        self.assertEqual("int", typename)
        self.assertEqual("ddepth", varname)

    # noinspection PyPep8,SpellCheckingInspection
    def test_get_arg_name_and_type_enum(self):
        html_type = """<td class="paramtype">int&nbsp;</td>"""
        # noinspection PyPep8
        html_name = """
          <td class="paramname">
            <em>borderType</em> = 
            <code><a class="el" href="fixtures/group__core__array.html#gga209f2f4869e304c82d07739337eae7c5afe14c13a4ea8b8e3b3ef399013dbae01">BORDER_DEFAULT</a></code>
            &nbsp;
          </td>"""
        typename, varname = FunctionTemplate.get_arg_name_and_type(html.fromstring(html_type),
                                                                   html.fromstring(html_name))
        self.assertEqual("BorderTypes", typename)
        self.assertEqual("borderType", varname)

    def test_create_function(self):
        self.func_template = FunctionTemplate(html.fromstring(self.filter_fragment, base_url=FIXTURES_FILTER_HTML))
        function = self.func_template.create_function()
        self.assertEqual(cv2.pyrDown, function.func)
        self.assertListEqual(["image1"], [r.name for r in function.results])

    def test_from_url(self):
        _, funcs = FunctionTemplate.from_url("d4/d86/group__imgproc__filter.html")
        with self.subTest("output types"):
            self.assertSetEqual(set(), FunctionTemplate.MISSING_OUTPUT_TYPES)
        with self.subTest("input types"):
            self.assertSetEqual(set(), FunctionTemplate.MISSING_INPUT_TYPES)
        with self.subTest("function count"):
            self.assertEqual(24, len(funcs))
