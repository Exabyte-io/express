from express.properties.non_scalar.two_dimensional_plot import TwoDimensionalPlotProperty


class ReactionEnergyProfile(TwoDimensionalPlotProperty):
    """
    Reaction energy profile.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        super(ReactionEnergyProfile, self).__init__(name, raw_data, *args, **kwargs)

        energies = [e or 0 for e in self.raw_data.get("reaction_energies", [])]

        #  convert reaction coordinate to float
        self.xDataArray = [x * (1.0 / len(energies)) for x in range(len(energies) + 1)]

        # offset reaction energies by initial
        self.yDataSeries = [[energies[i] - energies[0] for i in range(len(energies))]]
