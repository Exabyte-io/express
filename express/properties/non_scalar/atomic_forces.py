from express.properties.non_scalar import NonScalarProperty


class AtomicForces(NonScalarProperty):
    """
    Forces that is exerted on each atom by its surroundings.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(AtomicForces, self).__init__(name, parser, *args, **kwargs)
        self.atomic_forces = self.parser_data["atomic_forces"]

    def _serialize(self):
        return {
            'name': self.name,
            "units": self.property_schema.defaults["units"],
            "value": self.atomic_forces
        }
