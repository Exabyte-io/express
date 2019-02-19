from express.properties.scalar import ScalarProperty


class TotalForce(ScalarProperty):
    """
    Total force in the material.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(TotalForce, self).__init__(name, parser, *args, **kwargs)
        self.value = self.parser.total_force()
