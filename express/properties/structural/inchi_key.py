from express.properties.non_scalar import NonScalarProperty


class InchiKey(NonScalarProperty):
    """
    Inchi key property class.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(InchiKey, self).__init__(name, parser, *args, **kwargs)
        self.name = name
        self.value = self.parser.get_inchi_key()

    def _serialize(self):
        return self.value
