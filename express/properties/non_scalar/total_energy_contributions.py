from express.properties.non_scalar import NonScalarProperty


class TotalEnergyContributions(NonScalarProperty):
    """
    Total energy contribution factors.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(TotalEnergyContributions, self).__init__(name, parser, *args, **kwargs)

    def _serialize(self):
        data = {
            'name': self.name,
            'units': self.manifest["defaults"]["units"]
        }
        data.update(self.parser.total_energy_contributions())
        return data
