from express.properties.non_scalar import NonScalarProperty


class TotalEnergyContributions(NonScalarProperty):
    """
    Total energy contribution factors.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        super(TotalEnergyContributions, self).__init__(name, raw_data, *args, **kwargs)
        self.total_energy_contributions = self.raw_data["total_energy_contributions"]

    def _serialize(self):
        data = {
            'name': self.name,
            'units': self.esse.get_property_default_values(self.name)["units"]
        }
        data.update(self.total_energy_contributions)
        return data
