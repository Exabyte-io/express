import numpy as np
from express import settings


class RoundNumericValuesMixin(object):

    def _round(self, array, decimal_places=settings.PRECISION):
        return np.round(array, decimal_places).tolist()
