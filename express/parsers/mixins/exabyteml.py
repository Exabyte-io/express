from abc import abstractmethod


class ExabyteMLDataMixin(object):
    """
    Defines Exabyte ML interfaces.

    Note:
        THE FORMAT OF DATA STRUCTURE RETURNED MUST BE PRESERVED IN IMPLEMENTATION.
    """

    @abstractmethod
    def data_per_property(self):
        pass

    @abstractmethod
    def precision_per_property(self):
        pass

    @abstractmethod
    def scaling_params_per_feature(self):
        pass

    @abstractmethod
    def band_gaps_direct(self):
        pass

    @abstractmethod
    def band_gaps_indirect(self):
        pass
