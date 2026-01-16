from express.properties.non_scalar.two_dimensional_plot import TwoDimensionalPlotProperty


class WavefunctionAmplitude(TwoDimensionalPlotProperty):
    """
    Wavefunction amplitude.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(WavefunctionAmplitude, self).__init__(name, parser, *args, **kwargs)
        wavefunction_amplitude = self.parser.wavefunction_amplitude()
        self.xDataArray = wavefunction_amplitude[0]
        self.yDataSeries = [wavefunction_amplitude[1]]

