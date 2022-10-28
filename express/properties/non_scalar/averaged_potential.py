import numpy as np
from scipy.signal import find_peaks
from express.properties.non_scalar import NonScalarProperty


class AveragedPotential(NonScalarProperty):
    """
    Holds planar and macroscopic average of a potential (e.g. electrostatic potential).
    Additionally, minima are included as they can be of further use (e.g. potential lineup method).
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(AveragedPotential, self).__init__(name, parser, *args, **kwargs)
        self.data = self.safely_invoke_parser_method("averaged_potential")
        self.peak_prominence = [0.3, None]  # minimum and maximum required prominence (see _find_minima)

    def _serialize(self) -> dict:
        return {
            "name": self.name,
            "macroscopicMinima": self._find_minima(self.data["m_x"])
        }

    def _find_minima(self, array: np.ndarray) -> dict:
        # negate array to find minima
        peaks, _ = find_peaks(-1 * array, prominence=self.peak_prominence)

        return {
            "xDataArray": [self.data["x"][i] for i in np.nditer(peaks)],
            "yDataSeries": [[array[i] for i in np.nditer(peaks)]],
        }
