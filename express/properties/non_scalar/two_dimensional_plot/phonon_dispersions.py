from express.properties.non_scalar.two_dimensional_plot import TwoDimensionalPlotProperty


class PhononDispersions(TwoDimensionalPlotProperty):
    """
    Describes the frequencies and shapes of possible atomic oscillations inside a material.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(PhononDispersions, self).__init__(name, parser, *args, **kwargs)
        phonon_dispersions = self.parser.phonon_dispersions()
        self.xDataArray = phonon_dispersions['qpoints']
        self.yDataSeries = phonon_dispersions['frequencies']
