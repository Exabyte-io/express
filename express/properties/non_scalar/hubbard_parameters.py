from express.properties.non_scalar import NonScalarProperty


class HubbardParameters(NonScalarProperty):
    def __init__(self, name, parser, *args, **kwargs):
        super(HubbardParameters, self).__init__(name, parser, *args, **kwargs)

    def _serialize(self):
        return {
            "name": self.name,
            "units": self.manifest["defaults"]["units"],
            "category": self.parser.hubbard_parameters()["category"],
            "headers": self.parser.hubbard_parameters()["headers"],
            "values": self.parser.hubbard_parameters()["values"],
        }
