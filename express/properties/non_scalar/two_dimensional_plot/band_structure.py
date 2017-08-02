import numpy as np

from express.properties.utils import eigenvalues
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
        self.nspins = self.raw_data["nspins"]
        self.ibz_k_points = self.raw_data["ibz_k_points"]
        self.eigenvalues_at_kpoints = self.raw_data["eigenvalues_at_kpoints"]
        self.nkpoints = len(self.eigenvalues_at_kpoints)
        self.bands = self._get_band()
        self.xDataArray = self.ibz_k_points.tolist()
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
