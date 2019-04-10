import numpy as np

from express.properties.utils import eigenvalues
from express.settings import ZERO_WEIGHT_KPOINT_THRESHOLD
from express.properties.non_scalar.two_dimensional_plot import TwoDimensionalPlotProperty


class BandStructure(TwoDimensionalPlotProperty):
    """
    Describes the ranges of energy that an electron within the solid may have (called energy bands, allowed bands,
    or simply bands) and ranges of energy that it may not have (called band gaps or forbidden bands). By having
    'user' boolean type argument one could get the user defined band structure or the default one respectively. This
    is a complex property containing energy values for a number of electronic bands on a path in a three-dimensional
    reciprocal space.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(BandStructure, self).__init__(name, parser, *args, **kwargs)
        self.nspins = self.parser.nspins()

        self.eigenvalues_at_kpoints = self.parser.eigenvalues_at_kpoints()
        if kwargs.get("remove_non_zero_weight_kpoints", False):
            self.eigenvalues_at_kpoints = [e for e in self.eigenvalues_at_kpoints if e['weight'] <= ZERO_WEIGHT_KPOINT_THRESHOLD]

        self.nkpoints = len(self.eigenvalues_at_kpoints)
        self.bands = self._get_band()
        self.xDataArray = [eigenvalueData["kpoint"] for eigenvalueData in self.eigenvalues_at_kpoints]
        self.yDataSeries = self.bands.tolist()

    def _serialize(self):
        data = super(BandStructure, self)._serialize()
        data.update({'spin': [0.5, -0.5] * len(self.bands) if self.nspins > 1 else [0.5] * len(self.bands)})
        return data

    def _get_band(self):
        """
        Returns bands.

        Returns:
            ndarray
        """
        bands = np.array([[eigenvalues(self.eigenvalues_at_kpoints, k, s) for s in range(self.nspins)] for k in range(self.nkpoints)])
        bands = np.transpose(bands).reshape(len(bands[0][0]) * self.nspins, self.nkpoints)
        return bands
