from unittest import TestCase

from lxml import html

from functions import ParameterTemplate, ParamType

FIXTURES_FILTER_HTML = "/usr/share/doc/opencv-doc/opencv4/html/d4/d86/group__imgproc__filter.html"
FIXTURES_FRAGMENT_HTML = "fixtures/filter_fragment.html"


class TestParameterTemplate(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        ParamType.initialise()

    def test_get_arg_name_and_type_linked(self):
        html_type = """
          <td class="paramtype">
            <a class="el" href="../../dc/d84/group__core__basic.html">OutputArray</a>
            &nbsp;
          </td>"""
        html_name = """<td class="paramname"><em>dst</em>, </td>"""
        html_desc = """<td>output image of the same size and type as src. </td>"""
        param = ParameterTemplate.from_html_fragments(html.fromstring(html_name),
                                                      html.fromstring(html_type),
                                                      html.fromstring(html_desc))
        self.assertEqual("Array", param.type.name)
        self.assertEqual("dst", param.name)
        self.assertEqual("output image of the same size and type as src.", param.description)

    def test_get_arg_name_and_type_unlinked(self):
        html_type = """<td class="paramtype">int&nbsp;</td>"""
        html_name = """<td class="paramname"><em>ddepth</em>, </td>"""
        html_desc = """<td>depth of image. </td>"""
        param = ParameterTemplate.from_html_fragments(html.fromstring(html_name),
                                                      html.fromstring(html_type),
                                                      html.fromstring(html_desc))
        self.assertEqual("ddepth", param.name)
        self.assertEqual("depth of image.", param.description)
        self.assertEqual("int", param.type.name)

    # noinspection PyPep8,SpellCheckingInspection
    def test_get_arg_name_and_type_enum(self):
        html_type = """<td class="paramtype">int&nbsp;</td>"""
        html_name = ("""
          <td class="paramname">
            <em>borderType</em> = 
            <code><a class="el" href="../../d2/de8/group__core__array.html#gga209f2f4869e304c82d07739337""" +
                     """eae7c5afe14c13a4ea8b8e3b3ef399013dbae01">BORDER_DEFAULT</a></code>
            &nbsp;
          </td>""")
        html_desc = """<td>border type. </td>"""
        param = ParameterTemplate.from_html_fragments(html.fromstring(html_name, base_url=FIXTURES_FILTER_HTML),
                                                      html.fromstring(html_type, base_url=FIXTURES_FILTER_HTML),
                                                      html.fromstring(html_desc, base_url=FIXTURES_FILTER_HTML))
        self.assertEqual("borderType", param.name)
        self.assertEqual("border type.", param.description)
        self.assertEqual("BorderTypes", param.type.name)


# noinspection PyPep8Naming
def setUpClass() -> None:
    ParamType.initialise()
