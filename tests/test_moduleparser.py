from unittest import TestCase

from functions import ParamType
from parser.moduleparser import ModuleParser


class TestModuleParser(TestCase):
    def setUp(self) -> None:
        self.parser = ModuleParser()

    def test_get_root_modules(self):
        modules = self.parser.get_root_modules()
        names = [self.parser.get_module_name(x) for x in modules]
        for name in names:
            with self.subTest(f"Checking module '{name}' is whitelisted"):
                self.assertTrue(any(name.startswith(x) for x in ModuleParser.MODULE_WHITELIST))
        for white in ModuleParser.MODULE_WHITELIST:
            with self.subTest(f"Checking Whitelist: '{white}' found"):
                self.assertTrue(any(name.startswith(white) for name in names))

    def test_get_modules(self):
        root_mod = self.parser.get_modules()
        print(ParamType.MISSING_TYPES)
        print(f"Functions found: {root_mod.count()}")
