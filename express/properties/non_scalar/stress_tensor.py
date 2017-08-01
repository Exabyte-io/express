from express.properties.non_scalar import NonScalarProperty


class StressTensor(NonScalarProperty):
    """
    3x3 matrix expressing stresses in x, y and z dimensions.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(StressTensor, self).__init__(name, parser, *args, **kwargs)
        self.stress_tensor = self.parser_data["stress_tensor"]

    def _serialize(self):
        return {
            'name': self.name,
            "units": self.property_schema.defaults["units"],
            "value": self.stress_tensor
        }
