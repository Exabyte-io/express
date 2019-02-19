from express.properties.non_scalar import NonScalarProperty


class Symmetry(NonScalarProperty):
    """
    Symmetry property class.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(Symmetry, self).__init__(name, parser, *args, **kwargs)

    def _serialize(self):
        return {
            "spaceGroupSymbol": self.parser.space_group_symbol()["value"],
            "tolerance": {
                "value": self.parser.space_group_symbol()["tolerance"],
                "units": "angstrom"
            },
            "name": self.name
        }
