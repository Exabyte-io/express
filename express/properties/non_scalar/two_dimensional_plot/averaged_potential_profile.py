from express.properties.non_scalar.two_dimensional_plot import TwoDimensionalPlotProperty


class AveragedPotentialProfile(TwoDimensionalPlotProperty):
    """
    Averaged potential profile plot.
    """

    def __init__(self, name: str, parser, *args, **kwargs):
        super().__init__(name, parser, *args, **kwargs)

        self.data = self.safely_invoke_parser_method("averaged_potential")
        self.xDataArray = self.data["x"].tolist()
        self.yDataSeries = [self.data["planar_average"].tolist(), self.data["macroscopic_average"].tolist()]
