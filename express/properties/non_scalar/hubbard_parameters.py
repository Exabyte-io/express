from express.properties.non_scalar import NonScalarProperty


class HubbardParameters(NonScalarProperty):
    def __init__(self, name, parser, *args, **kwargs):
        super(HubbardParameters, self).__init__(name, parser, *args, **kwargs)

    def _serialize(self):
        return {
            "name": self.name,
            "units": self.manifest["defaults"]["units"],
            "values": self.parser.hubbard_parameters(),
        }
