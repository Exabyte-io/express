from express.properties.scalar import ScalarProperty


class TotalEnergy(ScalarProperty):
    """
    The ground state energy of the system.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(TotalEnergy, self).__init__(name, parser, *args, **kwargs)
        self.value = self.parser.total_energy()
