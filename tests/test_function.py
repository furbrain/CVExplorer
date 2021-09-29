from unittest import TestCase, mock
from unittest.mock import Mock

from datatypes import OutputData
from functions import Function, ParameterTemplate
from gui.pane import FunctionPane


class DummyControl:
    def __init__(self, default):
        self.default = default

    # noinspection PyPep8Naming
    def GetValue(self):
        return self.default

    # noinspection PyPep8Naming
    def GetCode(self):
        return repr(self.default)


class MockResult(OutputData):
    def __init__(self, name, data):
        super().__init__(name)
        self.data = data

    def display(self):
        return None


# noinspection PyTypeChecker
class TestFunction(TestCase):
    def setUp(self) -> None:
        """reset all properties of Function class"""
        Function.ALL = []
        self.function_list = []
        self.pane: Mock = mock.create_autospec(FunctionPane)

    def createFixtures(self):
        self.f1 = Function("Function1", Mock(return_value=(0, 2)), [
            ParameterTemplate("filename", str, "Filename to load", "filename.jpg"),
            ParameterTemplate("mode", int, default=1)
        ], [
                               # results
                               MockResult("image1", 0),
                               MockResult("result", 2)
                           ])
        self.f2 = Function("Function2", Mock(), [
            ParameterTemplate("filename", str, "Filename to load", ""),
            ParameterTemplate("mode", int)
        ], [
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

    def test_call(self):
        self.createFixtures()
        self.f1.call({})
        # noinspection PyUnresolvedReferences
        self.f1.func.assert_called_once()

    def test_get_code(self):
        self.createFixtures()
        params = {"filename": "'filename.jpg'", "mode": "1"}
        self.assertEqual("image1, result = cv2.Function1(filename='filename.jpg', mode=1)", self.f1.as_code(params))
