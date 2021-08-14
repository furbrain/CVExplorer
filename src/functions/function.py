from typing import Callable, Dict, Tuple, List, Type, Any

import wx

from datatypes.base import BaseData, ParamsInstance
from gui.pane import FunctionPane


class Function:
    def __init__(self, name: str, func: Callable, params: Dict[str, Tuple], results: List[BaseData]):
        self.name = name
        self.func = func
        self.param_template = params
        self.results: List[BaseData] = results
        self.params: ParamsInstance = {}
        self.instantiated = False

    def instantiate(self, pane: FunctionPane):
        self.params = pane.add_input_params(self.param_template)
        for result in self.results:
            result.params = pane.add_output_params(result.__class__.__name__, result.PARAMS)

    def call(self):
        args = [ctrl.GetValue() for ctrl in self.params.values()]
        results = self.func(*args)
        if len(self.results) == 1:
            self.results[0].data = results
        elif len(self.results) == len(results):
            for result, temp_result in zip(self.results, results):
                result.data = temp_result
        else:
            raise TypeError("Wrong number of results returned")
