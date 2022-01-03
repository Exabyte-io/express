from express.properties.non_scalar import NonScalarProperty


class Symmetry(NonScalarProperty):
    """
    Symmetry property class.
    """

    def __init__(self, name, parser, is_non_periodic=False, *args, **kwargs):
        super(Symmetry, self).__init__(name, parser, is_non_periodic, *args, **kwargs)
        self.is_non_periodic = is_non_periodic

    def _serialize(self):
        if self.is_non_periodic == False:
            return {
                "spaceGroupSymbol": self.parser.space_group_symbol()["value"],
                "tolerance": {
                    "value": self.parser.space_group_symbol()["tolerance"],
                    "units": "angstrom"
                },
                "name": self.name
            }
        else:
            return {
                "pointGroupSymbol": self.parser.point_group_symbol()['value'],
                "tolerance": {
                    "value": self.parser.point_group_symbol()["tolerance"],
                    "units": "angstrom"
                },
                "name": self.name
            }
