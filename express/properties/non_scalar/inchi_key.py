from express.properties.non_scalar import NonScalarProperty


class InchiKey(NonScalarProperty):
    """
    Inchi property class.
    """
    def __init__(self, name, parser, *args, **kwargs):
        super(InchiKey, self).__init__(name, parser, *args, **kwargs)
        inchi_run = self.parser.get_inchi_run()
        if inchi_run == 0:
            self.value = self.parser.get_inchi_key_null()
        else:
            self.value = self.parser.get_inchi_key()
