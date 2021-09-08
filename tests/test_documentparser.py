from unittest import TestCase

from parser import DocumentParser


class TestDocumentParser(TestCase):
    def test_get_function_templates(self):
        _, funcs = DocumentParser("d4/d86/group__imgproc__filter.html").get_function_templates()
        from functions import ParamType
        with self.subTest("missing types"):
            self.assertSetEqual(set(), ParamType.MISSING_TYPES)
        with self.subTest("function count"):
            self.assertEqual(22, len(funcs))
