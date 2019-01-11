from express.properties.non_scalar import NonScalarProperty


class ConvergenceElectronic(NonScalarProperty):
    """
    Convergence electronic.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(ConvergenceElectronic, self).__init__(name, parser, *args, **kwargs)
        self.convergence_electronic = self.raw_data["convergence_electronic"]

    def _serialize(self):
        return {
            'name': self.name,
            'units': self.manifest["units"],
            'data': self.convergence_electronic
        }
