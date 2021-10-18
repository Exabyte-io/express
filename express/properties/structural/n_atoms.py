from express.properties.non_scalar import NonScalarProperty


class NAtoms(NonScalarProperty):
    """
    Number of Atoms property class
    """
    def __init__(self, name, parser, *args, **kwargs):
        super().__init__(name, parser, *args, **kwargs)
        self.name = name
        self.n_atoms= self.parser.n_atoms()

    def _serialize(self):
        return self.value
