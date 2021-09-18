import importlib
import inspect
import pkgutil
import types
from typing import List

from functions import FunctionTemplate, Module
from parser.codefunctionparser import CodeFunctionParser


class CodeParser:
    PACKAGE_ROOT = 'utils'

    def __init__(self):
        package = importlib.import_module(self.PACKAGE_ROOT)
        found_pkgs = pkgutil.walk_packages(package.__path__)
        self.module_names = [f"{package.__name__}.{name}" for _, name, ispkg in found_pkgs]

    @staticmethod
    def get_functions(mod: types.ModuleType) -> List[FunctionTemplate]:
        func: types.FunctionType
        funcs_list: List[FunctionTemplate] = []
        for name, func in inspect.getmembers(mod, inspect.isfunction):
            parser = CodeFunctionParser(func)
            funcs_list.append(parser.get_template())
        return funcs_list

    def get_modules(self):
        for mod in self.module_names:
            module = importlib.import_module(mod)
            return Module(mod, [], self.get_functions(module))
