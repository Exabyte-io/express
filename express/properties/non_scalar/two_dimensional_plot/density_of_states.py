from express.properties.non_scalar.two_dimensional_plot import TwoDimensionalPlotProperty


class DensityOfStates(TwoDimensionalPlotProperty):
    """
    Describes the number of electronic states per interval of energy at each energy level that are available to be
    occupied. There are also projections of total electronic density onto each of the atomic states that are often
    useful.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        super(DensityOfStates, self).__init__(name, raw_data, *args, **kwargs)
        self.dos = self.raw_data["dos"]
        self.legend = [{}] + self.dos['partial_info']
        self.xDataArray = [self.dos['energy']]
        self.yDataSeries = [self.dos['total']]
        self.yDataSeries.extend([pdos for pdos in self.dos['partial']])
