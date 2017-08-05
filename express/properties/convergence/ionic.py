from express.properties.non_scalar import NonScalarProperty


class ConvergenceIonic(NonScalarProperty):
    """
    Convergence ionic.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(ConvergenceIonic, self).__init__(name, parser, *args, **kwargs)
        self.convergence_ionic = self.raw_data["convergence_ionic"]

    def _serialize(self):
        return {
            'name': self.name,
            'units': self.esse.get_schema_default_values(self.name)["units"],
            'data': self.convergence_ionic
        }
