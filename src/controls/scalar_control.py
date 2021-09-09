# noinspection PyPep8Naming
from controls.composite import CompositeControl


class ScalarControl(CompositeControl):
    @classmethod
    def get_fields(cls):
        from functions import ParameterTemplate
        fields = [
            ParameterTemplate("R", "int", default=0),
            ParameterTemplate("G", "int", default=0),
            ParameterTemplate("B", "int", default=0),
            ParameterTemplate("Alpha", "int", default=0),
        ]
        return fields
