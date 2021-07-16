from express.properties.non_scalar import NonScalarProperty


class Inchi(NonScalarProperty):
    """
    Inchi property class.
    """
    def __init__(self, name, parser, *args, **kwargs):
        super(Inchi, self).__init__(name, parser, *args, **kwargs)
        self.name = name
        print("self.name = {}".format(self.name))
        inchi_run = self.parser.get_inchi_run()
        if inchi_run == 0:
            self.value = self.parser.get_inchi_null()
        else:
            self.value = self.parser.get_inchi()
        print(self.name)
        print(self.value)

    def _serialize(self):
        return {
            "name": self.name,
            "value": self.value,
        }
