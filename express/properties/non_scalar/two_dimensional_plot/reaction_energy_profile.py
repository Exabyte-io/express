from express.properties.non_scalar.two_dimensional_plot import TwoDimensionalPlotProperty


class ReactionEnergyProfile(TwoDimensionalPlotProperty):
    """
    Reaction energy profile.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(ReactionEnergyProfile, self).__init__(name, parser, *args, **kwargs)
        self.xDataArray = self.parser.reaction_coordinates()
        self.yDataSeries = [self.parser.reaction_energies()]
