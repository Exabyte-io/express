from express.properties.scalar import ScalarProperty


class Pressure(ScalarProperty):
    """
    Scalar average pressure.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(Pressure, self).__init__(name, parser, *args, **kwargs)
        self.value = self.parser.pressure()
