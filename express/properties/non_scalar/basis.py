from express.properties.non_scalar import NonScalarProperty


class Basis(NonScalarProperty):
    """
    Defines elemental and geometrical constitution of the unit cell.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(Basis, self).__init__(name, parser, *args, **kwargs)
        self.basis = self.parser_data["basis"]

    def _serialize(self):
        serialized_data = self.basis
        serialized_data.update({
            "name": self.name,
            "units": self.esse.get_schema_default_values(self.name)["units"]
        })
        return serialized_data
