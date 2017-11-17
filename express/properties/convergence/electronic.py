from express.properties.non_scalar import NonScalarProperty


class ConvergenceElectronic(NonScalarProperty):
    """
    Convergence electronic.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(ConvergenceElectronic, self).__init__(name, parser, *args, **kwargs)
        self.convergence_electronic = self.raw_data["convergence_electronic"]

    def _serialize(self):
        data = []
        for step, energies in enumerate(self.convergence_electronic):
            for energy in energies:
                data.append({
                    "step": step,
                    "value": energy
                })
        return {
            'name': self.name,
            'units': self.esse.get_property_default_values(self.name)["units"],
            'data': data
        }
