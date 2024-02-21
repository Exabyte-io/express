import numpy as np
from express import settings


class RoundNumericValuesMixin(object):
    def _round(self, array):
        return np.round(array, settings.PRECISION).tolist()
