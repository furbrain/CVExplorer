from .composite import CompositeControl


class PointControl(CompositeControl):
    @classmethod
    def get_fields(cls):
        from functions import ParameterTemplate
        fields = [
            ParameterTemplate("X", "int", default=-1),
            ParameterTemplate("Y", "int", default=-1)
        ]
        return fields
