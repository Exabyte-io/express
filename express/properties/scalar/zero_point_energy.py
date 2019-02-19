from express.properties.scalar import ScalarProperty


class ZeroPointEnergy(ScalarProperty):
    """
    Zero point energy property class.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(ZeroPointEnergy, self).__init__(name, parser, *args, **kwargs)
        self.value = self.parser.zero_point_energy()
