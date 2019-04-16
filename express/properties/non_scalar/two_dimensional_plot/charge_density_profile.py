from express.properties.non_scalar.two_dimensional_plot import TwoDimensionalPlotProperty


class ChargeDensityProfile(TwoDimensionalPlotProperty):
    """
    Charge Density profile.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(ChargeDensityProfile, self).__init__(name, parser, *args, **kwargs)
        charge_density_profile = self.parser.charge_density_profile()
        self.xDataArray = charge_density_profile[0]
        self.yDataSeries = [charge_density_profile[1]]
