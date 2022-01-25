from express.properties.scalar import ScalarProperty


class SymmetrySymbolSpaceGroup(ScalarProperty):
    """
    Space Group Symmetry property class.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(SymmetrySymbolSpaceGroup, self).__init__(name, parser, *args, **kwargs)

    def _serialize(self):
        return {
            "value": self.parser.symmetry_symbol_space_group()["value"],
            "tolerance": self.parser.symmetry_symbol_space_group()["tolerance"],
            "name": self.name
        }

