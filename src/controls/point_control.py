from controls.composite import CompositeControl


class PointControl(CompositeControl):
    @classmethod
    def get_fields(cls):
        from functions import ParameterTemplate
        fields = [
            ParameterTemplate("Width", "int", default=-1),
            ParameterTemplate("Height", "int", default=-1)
        ]
        return fields
