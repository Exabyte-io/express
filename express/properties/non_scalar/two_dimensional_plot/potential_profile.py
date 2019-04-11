from express.properties.non_scalar.two_dimensional_plot import TwoDimensionalPlotProperty


class PotentialProfile(TwoDimensionalPlotProperty):
    """
    Potential profile.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(PotentialProfile, self).__init__(name, parser, *args, **kwargs)
        potential_profile = self.parser.potential_profile()
        self.xDataArray = potential_profile[0]
        self.yDataSeries = [potential_profile[1], potential_profile[2], potential_profile[3]]
