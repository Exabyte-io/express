from express.properties.non_scalar import NonScalarProperty


class Symmetry(NonScalarProperty):
    """
    Symmetry property class.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        super(Symmetry, self).__init__(name, raw_data, *args, **kwargs)

    def _serialize(self):
        return {
            "spaceGroupSymbol": self.raw_data["space_group_symbol"]["value"],
            "tolerance": {
                "value": self.raw_data["space_group_symbol"]["tolerance"],
                "units": "angstrom"
            },
            "name": self.name
        }
