from express.parsers import BaseParser
from express.parsers.mixins.exabyteml import ExabyteMLDataMixin


class ExabyteMLParser(BaseParser, ExabyteMLDataMixin):
    """
    Exabyte ML parser class.
    """

    def __init__(self, *args, **kwargs):
        super(ExabyteMLParser, self).__init__(*args, **kwargs)
        self.dataPerProperty = kwargs.get("dataPerProperty")
        self.predictedProperties = self.kwargs.get("predictedProperties")
        self.precisionPerProperty = kwargs.get("precisionPerProperty")
        self.scalingParamsPerFeature = kwargs.get("scalingParamsPerFeature")

    def data_per_property(self):
        return self.dataPerProperty

    def precision_per_property(self):
        return self.precisionPerProperty

    def scaling_params_per_feature(self):
        return self.scalingParamsPerFeature

    def band_gaps_direct(self):
        return next((i["value"] for i in self.predictedProperties if i["name"] == "band_gaps:direct"))

    def band_gaps_indirect(self):
        return next((i["value"] for i in self.predictedProperties if i["name"] == "band_gaps:indirect"))
