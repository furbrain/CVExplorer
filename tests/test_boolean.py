from unittest import TestCase

from datatypes import BooleanData


class TestBooleanData(TestCase):
    def test_display_true(self):
        b = BooleanData("test")
        b.data = True
        self.assertEqual("True", b.display())

    def test_display_false(self):
        b = BooleanData("test")
        b.data = False
        self.assertEqual("False", b.display())


