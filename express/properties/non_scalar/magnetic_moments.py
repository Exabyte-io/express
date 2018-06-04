from express.properties.non_scalar import NonScalarProperty


class MagneticMoments(NonScalarProperty):

    def __init__(self, name, raw_data, *args, **kwargs):
        super(MagneticMoments, self).__init__(name, raw_data, *args, **kwargs)
        self.magnetic_moments = self.raw_data["magnetic_moments"]

    def _serialize(self):
        return {
            'name': self.name,
            "units": self.esse.get_property_default_values(self.name)["units"],
            "values": [{"id": index + 1, "value": value} for index, value in enumerate(self.magnetic_moments)]
        }
