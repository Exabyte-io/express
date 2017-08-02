from express.properties.scalar import ScalarProperty


class TotalForce(ScalarProperty):
    """
    Total force in the material.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        super(TotalForce, self).__init__(name, raw_data, *args, **kwargs)
        self.value = self.raw_data["total_force"]
