from express.properties.non_scalar import NonScalarProperty


class StressTensor(NonScalarProperty):
    """
    3x3 matrix expressing stresses in x, y and z dimensions.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        super(StressTensor, self).__init__(name, raw_data, *args, **kwargs)
        self.stress_tensor = self.raw_data["stress_tensor"]

    def _serialize(self):
        return {
            'name': self.name,
            "units": self.manifest["defaults"]["units"],
            "value": self.stress_tensor
        }
