from express.properties.non_scalar import NonScalarProperty


class MaxRadii(NonScalarProperty):
    """
    Max Radii property class
    """
    def __init__(self, name, parser, *args, **kwargs):
        super().__init__(name, parser, *args, **kwargs)
        self.name = name
        self.max_radii = self.parser.max_radii()

    def _serialize(self):
        return self.value
