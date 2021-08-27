from unittest import TestCase, mock
from unittest.mock import call, Mock

import gui
from datatypes import BaseData
from functions import Function


class DummyControl:
    pass


class MockResult(BaseData):
    def __init__(self, name, data):
        super().__init__(name)
        self.data = data

    def display(self):
        return None


class TestFunction(TestCase):
    def setUp(self) -> None:
        """reset all properties of Function class"""
        Function.ALL = []
        self.function_list = []
        self.pane: Mock = mock.create_autospec(gui.FunctionPane)

    def createFixtures(self):
        self.f1 = Function("Function1", Mock(return_value=(0, 2)), {
            # parameters
            "param1": ({"filename": (DummyControl, {"value": 0})},),
            "param2": ({"mode": (DummyControl, {"val": 1})},)
        }, [
                               # results
                               MockResult("image1", 0),
                               MockResult("result", 2)
                           ])
        self.f2 = Function("Function1", Mock(), {
            # parameters
            "param1": ({"filename": (DummyControl, {"value": ""})},),
            "param2": ({"mode": (DummyControl, {"val": 1})},)
        }, [
                               # results
                               MockResult("image2", 1),
                               MockResult("result2", 3)
                           ])
        self.function_list.append(self.f1)
        self.function_list.append(self.f2)

    def test_function_all_list(self):
        self.createFixtures()
        self.assertListEqual(Function.ALL, self.function_list)

    def test_get_all_vars(self):
        self.createFixtures()
        self.assertDictEqual(Function.get_all_vars(), {"image1": 0,
                                                       "image2": 1,
                                                       "result": 2,
                                                       "result2": 3})

    def test_instantiate(self):
        self.createFixtures()
        self.f1.instantiate(self.pane)
        self.pane.add_input_params.assert_called_with(self.f1.param_template)
        self.assertListEqual(self.pane.add_output_params.mock_calls, [call(x.name, x.PARAMS) for x in self.f1.results])
        self.pane.register_change_handler.assert_called_with(self.f1.on_changed)

    def test_on_changed(self):
        self.createFixtures()
        self.f1.instantiate(self.pane)
        self.f1.on_changed()
        # noinspection PyUnresolvedReferences
        self.f1.func.assert_called_once()
        self.pane.set_display.assert_called_with(None)

    def test_call(self):
        self.createFixtures()
        self.f1.call()
        # noinspection PyUnresolvedReferences
        self.f1.func.assert_called_once()
