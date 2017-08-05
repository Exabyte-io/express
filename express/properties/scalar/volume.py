from express.properties.scalar import ScalarProperty


class Volume(ScalarProperty):
    """
    Volume property class.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        super(Volume, self).__init__(name, raw_data, *args, **kwargs)
        self.value = self.raw_data["volume"]
