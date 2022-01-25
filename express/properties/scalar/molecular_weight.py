from express.properties.scalar import ScalarProperty


class MolecularWeight(ScalarProperty):
    """
    Molecular Weight property class.
    """
    def __init__(self, name, parser, *args, **kwargs):
        super(MolecularWeight, self).__init__(name, parser, *args, **kwargs)
        self.name = name
        self.value = self.parser.molecular_weight()

    def _serialize(self):
        return self.value
