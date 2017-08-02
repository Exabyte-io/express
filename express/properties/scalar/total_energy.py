from express.properties.scalar import ScalarProperty


class TotalEnergy(ScalarProperty):
    """
    The ground state energy of the system.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        super(TotalEnergy, self).__init__(name, raw_data, *args, **kwargs)
        self.value = self.raw_data["total_energy"]
