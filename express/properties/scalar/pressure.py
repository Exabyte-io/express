from express.properties.scalar import ScalarProperty


class Pressure(ScalarProperty):
    """
    Scalar average pressure.
    """

    def __init__(self, name, parser):
        super(Pressure, self).__init__(name, parser)
        self.value = self.parser_data["pressure"]
