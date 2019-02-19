from express.properties.non_scalar import NonScalarProperty


class StressTensor(NonScalarProperty):
    """
    3x3 matrix expressing stresses in x, y and z dimensions.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(StressTensor, self).__init__(name, parser, *args, **kwargs)

    def _serialize(self):
        return {
            'name': self.name,
            "units": self.manifest["defaults"]["units"],
            "value": self.parser.stress_tensor()
        }
