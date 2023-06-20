from express.properties.non_scalar import NonScalarProperty


class Inchi(NonScalarProperty):
    """
    Inchi property class.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(Inchi, self).__init__(name, parser, *args, **kwargs)
        self.name = name
        self.inchi_long, self.value = self.parser.get_inchi()

    def _serialize(self):
        return self.value
