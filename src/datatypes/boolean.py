from typing import Optional, TYPE_CHECKING

from .base import BaseData

if TYPE_CHECKING:
    pass


class BooleanData(BaseData):
    PARAMS = {
    }

    def __init__(self, name: str):
        super().__init__(name)
        self.data: Optional[bool] = None

    def display(self) -> bool:
        return self.data
