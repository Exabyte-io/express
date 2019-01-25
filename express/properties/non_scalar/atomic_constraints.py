from express.properties.non_scalar import NonScalarProperty


class AtomicConstraints(NonScalarProperty):
    """
    Atomic constraints property class.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        super(AtomicConstraints, self).__init__(name, raw_data, *args, **kwargs)
        self.atomic_constraints = self.raw_data["atomic_constraints"]

    def _serialize(self):
        return {
            'name': self.name,
            "values": [{"id": index + 1, "value": value} for index, value in enumerate(self.atomic_constraints)]
        }
