# noinspection PyPep8Naming
from controls.composite import CompositeControl


class TermCriteriaControl(CompositeControl):
    @classmethod
    def get_fields(cls):
        from functions import ParameterTemplate
        fields = [
            ParameterTemplate("Type", "int", default=3),
            ParameterTemplate("MaxCount", "int", default=5),
            ParameterTemplate("Epsilon", "float", default=1.0)
        ]
        return fields
