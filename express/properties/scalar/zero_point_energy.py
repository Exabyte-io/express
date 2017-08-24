from express.properties.scalar import ScalarProperty


class ZeroPointEnergy(ScalarProperty):
    """
    Zero point energy property class.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        super(ZeroPointEnergy, self).__init__(name, raw_data, *args, **kwargs)
        self.value = self.raw_data["zero_point_energy"]
