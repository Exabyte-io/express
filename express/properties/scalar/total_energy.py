from express.properties.scalar import ScalarProperty


class TotalEnergy(ScalarProperty):
    """
    The ground state energy of the system.
    """

    def __init__(self, name, parser):
        super(TotalEnergy, self).__init__(name, parser)
        self.value = self.parser_data["total_energy"]
