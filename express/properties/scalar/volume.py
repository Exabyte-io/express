from express.properties.scalar import ScalarProperty


class Volume(ScalarProperty):
    """
    Volume property class.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(Volume, self).__init__(name, parser, *args, **kwargs)
        self.value = self.parser.volume()
