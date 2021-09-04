from typing import Optional, TYPE_CHECKING

from .base import OutputData

if TYPE_CHECKING:
    pass


class BooleanData(OutputData):
    HANDLED_CLASSES = [bool]
    PARAMS = {
    }

    def __init__(self, name: str):
        super().__init__(name)
        self.data: Optional[bool] = None

    def display(self) -> str:
        return str(self.data)
