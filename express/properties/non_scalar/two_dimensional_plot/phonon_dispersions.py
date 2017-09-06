from express.properties.non_scalar.two_dimensional_plot import TwoDimensionalPlotProperty


class PhononDispersions(TwoDimensionalPlotProperty):
    """
    Describes the frequencies and shapes of possible atomic oscillations inside a material.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        super(PhononDispersions, self).__init__(name, raw_data, *args, **kwargs)
        phonon_bands = self.raw_data["phonon_bands"]
        self.xDataArray = phonon_bands['qpoints']
        self.yDataSeries = phonon_bands['frequencies']
