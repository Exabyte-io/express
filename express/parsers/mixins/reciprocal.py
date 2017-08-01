from abc import abstractmethod


class ReciprocalDataMixin(object):
    """
    Defines reciprocal interfaces.

    Note:
        THE FORMAT OF DATA STRUCTURE RETURNED MUST BE PRESERVED IN IMPLEMENTATION.
    """

    @abstractmethod
    def ibz_k_points(self):
        """
        Returns ibz_k_points.

        Returns:
             ndarray

        Example:
            [
                [  0.00000000e+00   0.00000000e+00   0.00000000e+00]
                [ -4.84710133e-17  -4.84710133e-17  -5.00000000e-01]
                [  0.00000000e+00  -5.00000000e-01   0.00000000e+00]
                [ -4.84710133e-17  -5.00000000e-01  -5.00000000e-01]
                [ -5.00000000e-01   6.58404272e-17   0.00000000e+00]
                [ -5.00000000e-01  -5.00000000e-01   0.00000000e+00]
            ]
        """
        pass
