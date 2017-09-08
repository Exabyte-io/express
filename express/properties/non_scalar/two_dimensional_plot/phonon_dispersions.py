from express.properties.non_scalar.two_dimensional_plot import TwoDimensionalPlotProperty


class PhononDispersions(TwoDimensionalPlotProperty):
    """
    Describes the frequencies and shapes of possible atomic oscillations inside a material.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        super(PhononDispersions, self).__init__(name, raw_data, *args, **kwargs)
        phonon_dispersions = self.raw_data["phonon_dispersions"]
        self.xDataArray = phonon_dispersions['qpoints']
        self.yDataSeries = phonon_dispersions['frequencies']
