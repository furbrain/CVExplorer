from typing import Callable, Dict, List, Any, TYPE_CHECKING, ClassVar

import attr

from .parameter import ParameterTemplate

if TYPE_CHECKING:
    from datatypes import OutputData


@attr.s(auto_attribs=True)
class Function:
    ALL: ClassVar[List["Function"]] = []
    name: str
    func: Callable
    param_template: List[ParameterTemplate]
    results: List["OutputData"]
    docs: str

    def __attrs_post_init__(self):
        self.ALL.append(self)

    @classmethod
    def get_all_vars(cls) -> Dict[str, Any]:
        return {result.name: result.data for func in Function.ALL for result in func.results}

    def call(self, args: Dict[str, Any]):
        results = self.func(**args)
        if len(self.results) == 1:
            self.results[0].data = results
        elif len(self.results) == len(results):
            for result, temp_result in zip(self.results, results):
                result.data = temp_result
        else:
            raise TypeError("Wrong number of results returned")

    def as_code(self, arg_codes: Dict[str, str]):
        result_names = ", ".join(result.name for result in self.results)
        param_values = ", ".join(f"{name}={param}" for name, param in arg_codes.items())
        return f"{result_names} = cv2.{self.name}({param_values})"

    def get_result(self, index):
        return self.results[index].display()

    def get_vars(self):
        return {r.name: r.data for r in self.results}
