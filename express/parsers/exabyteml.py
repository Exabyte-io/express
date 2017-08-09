from express.parsers import BaseParser
from express.parsers.mixins.exabyteml import ExabyteMLDataMixin


class ExabyteMLParser(BaseParser, ExabyteMLDataMixin):
    """
    Exabyte ML parser class.
    """

    def __init__(self, *args, **kwargs):
        super(ExabyteMLParser, self).__init__(*args, **kwargs)

    def model(self):
        """
        docstring: express.parsers.mixins.ml.MLDataMixin#model
        """
        return self.kwargs["model"].toDict()

    def units(self):
        """
        docstring: express.parsers.mixins.ml.MLDataMixin#units
        """
        return [u.toDict() for u in self.kwargs["units"]]
