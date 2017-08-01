from abc import abstractmethod


class IonicDataMixin(object):
    """
    Defines ionic interfaces.

    Note:
        THE FORMAT OF DATA STRUCTURE RETURNED MUST BE PRESERVED IN IMPLEMENTATION.
    """

    @abstractmethod
    def lattice(self):
        """
        Returns lattice.

        Returns:
            dict

        Example:
            {
                'vectors': {
                    'a': [-0.561154473, -0.000000000, 0.561154473],
                    'b': [-0.000000000, 0.561154473, 0.561154473],
                    'c': [-0.561154473, 0.561154473, 0.000000000],
                    'alat': 9.44858082
                }
             }
        """
        pass

    @abstractmethod
    def basis(self):
        """
        Returns basis.

        Returns:
            dict

        Example:
            {
                'units': 'bohr',
                'elements': [{'id': 1, 'value': 'Si'}, {'id': 2, 'value': 'Si'}],
                'coordinates': [{'id': 1, 'value': [0.0, 0.0, 0.0]}, {'id': 2, 'value': [0.0, 0.0, 0.0]}]
             }
        """
        pass

    @abstractmethod
    def convergence_ionic(self):
        """
        Extracts convergence ionic.

        Returns:
             list[dict]
        """
        pass

    @abstractmethod
    def stress_tensor(self):
        """
        Returns stress tensor.

        Returns:
            list

        Example:
            [
                [
                    0.00050115,
                    -1e-08,
                    0.0
                ],
                [
                    -1e-08,
                    0.0005011,
                    0.0
                ],
                [
                    0.0,
                    -0.0,
                    0.00050111
                ]
            ]
        """
        pass

    @abstractmethod
    def pressure(self):
        """
        Returns pressure.

        Returns:
            float

        Examples:
             73.72
        """
        pass

    @abstractmethod
    def total_force(self):
        """
        Returns total force.

        Returns:
            float

        Example:
            1e-06
        """
        pass

    @abstractmethod
    def atomic_forces(self):
        """
        Returns forces that is exerted on each atom by its surroundings.

        Returns:
            list

        Example:
            [
                [
                    -3.9e-07,
                    -2.4e-07,
                    0.0
                ],
                [
                    3.9e-07,
                    2.4e-07,
                    0.0
                ]
            ]
        """
        pass
