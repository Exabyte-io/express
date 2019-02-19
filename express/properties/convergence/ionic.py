from express.properties.non_scalar import NonScalarProperty


class ConvergenceIonic(NonScalarProperty):
    """
    Convergence ionic.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(ConvergenceIonic, self).__init__(name, parser, *args, **kwargs)

    def _serialize(self):
        return {
            'name': self.name,
            'units': self.manifest["defaults"]["units"],
            'data': self.parser.convergence_ionic()
        }
