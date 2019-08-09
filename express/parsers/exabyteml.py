from express.parsers import BaseParser
from express.parsers.mixins.exabyteml import ExabyteMLDataMixin


class ExabyteMLParser(BaseParser, ExabyteMLDataMixin):
    """
    Exabyte ML parser class.
    """

    def __init__(self, *args, **kwargs):
        super(ExabyteMLParser, self).__init__(*args, **kwargs)
        self.model = kwargs.get("model")
        self.targets = kwargs.get("targets")
        self.features = kwargs.get("features")
        self.predicted_properties = self.kwargs.get("predicted_properties")
        self.scaling_params_per_feature = kwargs.get("scaling_params_per_feature")

    def band_gaps_direct(self):
        return next((i["value"] for i in self.predicted_properties if i["name"] == "band_gaps:direct"))

    def band_gaps_indirect(self):
        return next((i["value"] for i in self.predicted_properties if i["name"] == "band_gaps:indirect"))
