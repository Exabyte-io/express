from express.properties.non_scalar import NonScalarProperty


class ConvergenceElectronic(NonScalarProperty):
    """
    Convergence electronic.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(ConvergenceElectronic, self).__init__(name, parser, *args, **kwargs)

    def _serialize(self):
        return {
            'name': self.name,
            'units': self.manifest["defaults"]["units"],
            'data': self.parser.convergence_electronic()
        }
