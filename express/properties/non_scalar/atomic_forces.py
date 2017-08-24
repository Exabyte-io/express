from express.properties.non_scalar import NonScalarProperty


class AtomicForces(NonScalarProperty):
    """
    Forces that is exerted on each atom by its surroundings.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        super(AtomicForces, self).__init__(name, raw_data, *args, **kwargs)
        self.atomic_forces = self.raw_data["atomic_forces"]

    def _serialize(self):
        return {
            'name': self.name,
            "units": self.esse.get_property_default_values(self.name)["units"],
            "values": [{"id": index + 1, "value": value} for index, value in enumerate(self.atomic_forces)]
        }
