from express.properties.scalar import ScalarProperty


class FermiEnergy(ScalarProperty):
    """
    The highest energy level occupied by electrons in a system.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        super(FermiEnergy, self).__init__(name, raw_data, *args, **kwargs)
        self.value = self.raw_data["fermi_energy"]
