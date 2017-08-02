from express.properties.scalar import ScalarProperty


class Pressure(ScalarProperty):
    """
    Scalar average pressure.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        super(Pressure, self).__init__(name, raw_data, *args, **kwargs)
        self.value = self.raw_data["pressure"]
