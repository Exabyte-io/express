from express.properties.non_scalar import NonScalarProperty


class SpaceGroupSymbol(NonScalarProperty):
    """
    Defines elemental and geometrical constitution of the unit cell.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        super(SpaceGroupSymbol, self).__init__(name, raw_data, *args, **kwargs)

    def _serialize(self):
        return {
            "name": self.name,
            "value": self.raw_data["space_group_symbol"]
        }
