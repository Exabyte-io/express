from express.properties.non_scalar import NonScalarProperty


class PointGroupSymmetry(NonScalarProperty):
    """
    Point Group Symmetry property class.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(PointGroupSymmetry, self).__init__(name, parser, *args, **kwargs)

    def _serialize(self):
        return {
            "value": self.parser.point_group_symbol()["value"],
            "tolerance": self.parser.point_group_symbol()["tolerance"],
            "name": self.name
        }

