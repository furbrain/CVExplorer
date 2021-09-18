from unittest import TestCase

from parser.codeparser import CodeParser


class TestCodeParser(TestCase):
    def setUp(self) -> None:
        self.parser = CodeParser()

    def test_get_modules(self):
        mods = self.parser.get_modules()
        print(mods)
