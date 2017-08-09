from express.parsers import BaseParser
from express.parsers.mixins.exabyteml import ExabyteMLDataMixin


class ExabyteExabyteMLParser(BaseParser, ExabyteMLDataMixin):
    """
    Exabyte ML parser class.
    """

    def __init__(self, *args, **kwargs):
        super(ExabyteExabyteMLParser, self).__init__(*args, **kwargs)
        self.model = kwargs["model"]
        self.units = kwargs["units"]

    def model(self):
        """
        docstring: express.parsers.mixins.ml.MLDataMixin#model
        """
        return self.model

    def units(self):
        """
        docstring: express.parsers.mixins.ml.MLDataMixin#units
        """
        return self.units
