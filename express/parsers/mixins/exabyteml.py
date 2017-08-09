from abc import abstractmethod


class ExabyteMLDataMixin(object):
    """
    Defines Exabyte ML interfaces.

    Note:
        THE FORMAT OF DATA STRUCTURE RETURNED MUST BE PRESERVED IN IMPLEMENTATION.
    """

    @abstractmethod
    def model(self):
        """
        Returns ML model parameters.

        Returns:
             dict
        """
        pass

    @abstractmethod
    def units(self):
        """
        Returns ML unit configs such as scale_and_reduce.

        Returns:
             dict
        """
        pass
