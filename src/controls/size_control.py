# noinspection PyPep8Naming
from controls.composite import CompositeControl


class SizeControl(CompositeControl):
    # noinspection PyTypeChecker
    @classmethod
    def get_fields(cls):
        from functions import ParameterTemplate
        fields = [
            ParameterTemplate("Width", int, default=3),
            ParameterTemplate("Height", int, default=3)
        ]
        return fields
