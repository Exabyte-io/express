from express.properties.non_scalar import NonScalarProperty


class SymmetrySymbolPointGroup(NonScalarProperty):
    """
    Point Group Symmetry property class.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(SymmetrySymbolPointGroup, self).__init__(name, parser, *args, **kwargs)

    def _serialize(self):
        return {
            "value": self.parser.symmetry_symbol_point_group()["value"],
            "tolerance": self.parser.symmetry_symbol_point_group()["tolerance"],
            "name": self.name
        }

