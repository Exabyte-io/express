from express.properties.scalar import ScalarProperty


class HOMOEnergy(ScalarProperty):
    """
    The highest occupied molecular orbital energy.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(HOMOEnergy, self).__init__(name, parser, *args, **kwargs)
        self.value = self.parser.homo_energy()
