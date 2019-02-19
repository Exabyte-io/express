from express.properties.scalar import ScalarProperty


class Density(ScalarProperty):
    """
    Density property class.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(Density, self).__init__(name, parser, *args, **kwargs)
        self.value = self.parser.density()
