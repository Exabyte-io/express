from express.properties.non_scalar.two_dimensional_plot import TwoDimensionalPlotProperty


class PhononDOS(TwoDimensionalPlotProperty):
    """
    Describes the number of vibrational modes per interval of energy.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(PhononDOS, self).__init__(name, parser, *args, **kwargs)
        phonon_dos = self.parser.phonon_dos()
        self.xDataArray = [phonon_dos['frequency']]
        self.yDataSeries = [phonon_dos['total']]
