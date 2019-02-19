from express.properties.non_scalar.two_dimensional_plot import TwoDimensionalPlotProperty


class DensityOfStates(TwoDimensionalPlotProperty):
    """
    Describes the number of electronic states per interval of energy at each energy level that are available to be
    occupied. There are also projections of total electronic density onto each of the atomic states that are often
    useful.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(DensityOfStates, self).__init__(name, parser, *args, **kwargs)
        dos = self.parser.dos()
        self.xDataArray = [dos['energy']]
        self.yDataSeries = [dos['total']]
        self.legend = [{}] + dos['partial_info']
        self.yDataSeries.extend([pdos for pdos in dos['partial']])
