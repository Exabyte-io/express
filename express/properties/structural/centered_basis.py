from express.properties.non_scalar import NonScalarProperty


class CenteredBasis(NonScalarProperty):
    """
    Inchi property class.
    """
    def __init__(self, name, parser, *args, **kwargs):
        super().__init__(name, parser, *args, **kwargs)
        self.name = name
        self.centered_basis = self.parser.center_of_mass_basis()

    def _serialize(self):
        return self.centered_basis
