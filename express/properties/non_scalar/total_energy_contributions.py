from express.properties.non_scalar import NonScalarProperty


class TotalEnergyContributions(NonScalarProperty):
    """
    Total energy contribution factors.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(TotalEnergyContributions, self).__init__(name, parser, *args, **kwargs)
        self.total_energy_contributions = self.parser_data["total_energy_contributions"]

    def _serialize(self):
        data = {
            'name': self.name,
            'units': self.property_schema.defaults["units"]
        }
        data.update(self.total_energy_contributions)
        return data
