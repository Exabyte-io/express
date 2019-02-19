from express.properties.scalar import ScalarProperty


class FermiEnergy(ScalarProperty):
    """
    The highest energy level occupied by electrons in a system.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(FermiEnergy, self).__init__(name, parser, *args, **kwargs)
        self.value = self.parser.fermi_energy()
