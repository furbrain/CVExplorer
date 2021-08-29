from typing import Callable, Dict, Tuple, List, Any, Optional, TYPE_CHECKING

from datatypes import BaseData, ParamsInstance
if TYPE_CHECKING:
    from gui import FunctionPane


class Function:
    ALL: List["Function"] = []

    def __init__(self, name: str, func: Callable, params: Dict[str, Tuple], results: List[BaseData]):
        self.name = name
        self.func = func
        self.param_template = params
        self.results: List[BaseData] = results
        self.params: ParamsInstance = {}
        self.pane: Optional[FunctionPane] = None
        self.ALL.append(self)

    @classmethod
    def get_all_vars(cls) -> Dict[str, Any]:
        return {result.name: result.data for func in Function.ALL for result in func.results}

    def instantiate(self, pane: "FunctionPane"):
        self.pane = pane
        self.params = pane.add_input_params(self.param_template)
        for result in self.results:
            result.params = pane.add_output_params(result.name, result.PARAMS)
        pane.register_change_handler(self.on_changed)

    # noinspection PyUnusedLocal
    def on_changed(self, event=None):
        try:
            self.call()
            results = self.results[0].display()
        except Exception as e:
            self.pane.set_display(e)
        else:
            self.pane.set_display(results)
        self.pane.Refresh()

    def call(self):
        args = {name: ctrl.GetValue() for name, ctrl in self.params.items()}
        results = self.func(**args)
        if len(self.results) == 1:
            self.results[0].data = results
        elif len(self.results) == len(results):
            for result, temp_result in zip(self.results, results):
                result.data = temp_result
        else:
            raise TypeError("Wrong number of results returned")
