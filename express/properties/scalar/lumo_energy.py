from express.properties.scalar import ScalarProperty


class LUMOEnergy(ScalarProperty):
    """
    The lowest unoccupied molecular orbital energy.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(LUMOEnergy, self).__init__(name, parser, *args, **kwargs)
        self.value = self.parser.lumo_energy()
