from express.properties.non_scalar.two_dimensional_plot import TwoDimensionalPlotProperty


class ReactionEnergyProfile(TwoDimensionalPlotProperty):
    """
    Reaction energy profile.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        super(ReactionEnergyProfile, self).__init__(name, raw_data, *args, **kwargs)
        self.xDataArray = self.raw_data.get("reaction_coordinates", [])
        self.yDataSeries = [self.raw_data.get("reaction_energies", [])]
