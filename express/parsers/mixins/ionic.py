from abc import abstractmethod


class IonicDataMixin(object):
    """
    Defines ionic interfaces.

    Note:
        THE FORMAT OF DATA STRUCTURE RETURNED MUST BE PRESERVED IN IMPLEMENTATION.
    """

    @abstractmethod
    def lattice_vectors(self):
        """
        Returns lattice vectors.

        Returns:
            dict

        Example:
            {
                'a': [-0.561154473, -0.000000000, 0.561154473],
                'b': [-0.000000000, 0.561154473, 0.561154473],
                'c': [-0.561154473, 0.561154473, 0.000000000],
                'alat': 9.44858082
             }
        """
        pass

    @abstractmethod
    def lattice_bravais(self):
        """
        Returns lattice bravais.

        Returns:
            dict

        Example:
            {
                "type": "CUB",
                "a": 5.14,
                "b": 5.14,
                "c": 5.14,
                "alpha": 90.0,
                "beta": 90.0,
                "gamma": 90.0,
                "units": {
                    "length": "angstrom",
                    "angle": "degree"
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
                'units': 'crystal',
                'elements': [{'id': 1, 'value': 'Si'}, {'id': 2, 'value': 'Si'}],
                'coordinates': [{'id': 1, 'value': [0.0, 0.0, 0.0]}, {'id': 2, 'value': [0.25, 0.25, 0.25]}]
             }
        """
        pass

    @abstractmethod
    def convergence_ionic(self):
        """
        Extracts convergence ionic.

        Returns:
             list[float]

        Example:
            [
                1.4018213061907816,
                0.5939946985677435,
                0.007003124785903934,
                0.0010198831091687887,
                0.000042041606287774244,
                0.000007619190783544846
              ]
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

    @abstractmethod
    def space_group_symbol(self):
        """
        Returns space group symbol.

        Returns:
             dict

        Example:
            {
                "value": "Fd-3m",
                "tolerance": 0.3
            }
        """
        pass

    @abstractmethod
    def formula(self):
        """
        Returns formula.

        Return:
             str

        Examples:
             SiGe
        """
        pass

    @abstractmethod
    def reduced_formula(self):
        """
        Returns reduced formula.

        Return:
             str

        Examples:
             SiGe
        """
        pass

    @abstractmethod
    def volume(self):
        """
        Returns volume.

        Returns:
             float

        Examples:
             1
        """
        pass

    @abstractmethod
    def elemental_ratios(self):
        """
        Returns elemental ratio.

        Returns:
             dict

        Examples:
            {
                "Si": 0.6,
                "Ge": 0.4
            }
        """
        pass

    @abstractmethod
    def density(self):
        """
        Returns density.

        Returns:
             float

        Examples:
             1
        """
        pass

    @abstractmethod
    def zero_point_energy(self):
        """
        Returns zero point energy.

        Returns:
             float

        Examples:
             73.72
        """
        pass

    @abstractmethod
    def phonon_dos(self):
        """
        Returns phonon dos.

        Returns:
             dict

        Example:
            {
                'frequency': [-1.2588E-05, 9.9999E-01, 2.0000E+00, 3.0000E+00, ....]
                'total': [0.0000E+00, 2.5386E-07, 1.0154E-06, 2.2847E-06, ....]
            }
        """
        pass

    @abstractmethod
    def phonon_dispersions(self):
        """
        Returns phonon dispersions.

        Returns:
             dict

        Example:
            {
                'qpoints': [[0.00, 0.00, 0.00],[0.00, 0.00, 0.01],....],
                'frequencies': [['-0.0000', '-0.0000', '-0.0000', '574.0778', '574.0778', '574.2923'],
                ['29.3716', '30.0630', '70.4699', '568.0790', '569.7664', '569.9710'], ....]
            }
        """
        pass
