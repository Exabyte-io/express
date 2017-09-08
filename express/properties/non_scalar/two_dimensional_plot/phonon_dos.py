from express.properties.non_scalar.two_dimensional_plot import TwoDimensionalPlotProperty


class PhononDOS(TwoDimensionalPlotProperty):
    """
    Describes the number of vibrational modes per interval of energy.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        super(PhononDOS, self).__init__(name, raw_data, *args, **kwargs)
        phonon_dos = self.raw_data["phonon_dos"]
        self.xDataArray = [phonon_dos['frequency']]
        self.yDataSeries = [phonon_dos['total']]
