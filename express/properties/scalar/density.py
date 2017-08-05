from express.properties.scalar import ScalarProperty


class Density(ScalarProperty):
    """
    Density property class.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        super(Density, self).__init__(name, raw_data, *args, **kwargs)
        self.value = self.raw_data["density"]
