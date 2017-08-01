from express.properties.scalar import ScalarProperty


class TotalForce(ScalarProperty):
    """
    Total force in the material.
    """

    def __init__(self, name, parser):
        super(TotalForce, self).__init__(name, parser)
        self.value = self.parser_data["total_force"]
