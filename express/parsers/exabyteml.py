from express.parsers import BaseParser
from express.parsers.mixins.exabyteml import ExabyteMLDataMixin


class ExabyteMLParser(BaseParser, ExabyteMLDataMixin):
    """
    Exabyte ML parser class.
    """

    def __init__(self, *args, **kwargs):
        super(ExabyteMLParser, self).__init__(*args, **kwargs)
        self.dataPerProperty = kwargs.get("dataPerProperty")
        self.precisionPerProperty = kwargs.get("precisionPerProperty")
        self.scalingParamsPerFeature = kwargs.get("scalingParamsPerFeature")

    def data_per_property(self):
        return self.dataPerProperty

    def precision_per_property(self):
        return self.precisionPerProperty

    def scaling_params_per_feature(self):
        return self.scalingParamsPerFeature
