from abc import abstractmethod


class IonicDataMixin(object):
    """
    Defines ionic interfaces.

    Note:
        THE FORMAT OF DATA STRUCTURE RETURNED MUST BE PRESERVED IN IMPLEMENTATION.
    """

    @abstractmethod
    def initial_lattice_vectors(self):
        """
        Returns initial lattice vectors.

        Units: angstrom

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
    def initial_basis(self):
        """
        Returns initial basis.

        Units: crystal

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
    def final_lattice_vectors(self):
        """
        Returns final lattice vectors.

        Units: angstrom

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
    def final_basis(self):
        """
        Returns final basis.

        Units: crystal

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

        Units:
            energy: eV

        Returns:
             list[dict]

        Example:
            [
                {
                    "electronic": {
                        "data": [
                            0.10304755,
                            0.04365706,
                            0.00051533,
                            0.00007517,
                            0.00000294,
                            6.7E-7
                        ],
                        "units": "eV"
                    },
                    "energy": -258.629394472941,
                    "structure": {
                        "basis": {
                            "coordinates": [
                                {
                                    "id": 0,
                                    "value": [
                                        0,
                                        0,
                                        0
                                    ]
                                },
                                {
                                    "id": 1,
                                    "value": [
                                        1.11631153838261,
                                        0.789351104951054,
                                        1.93350786347877
                                    ]
                                }
                            ],
                            "elements": [
                                {
                                    "id": 0,
                                    "value": "Si"
                                },
                                {
                                    "id": 1,
                                    "value": "Si"
                                }
                            ],
                            "units": "angstrom"
                        },
                        "lattice": {
                            "vectors": {
                                "a": [
                                    3.34893229493841,
                                    0,
                                    1.93350786347877
                                ],
                                "alat": 1,
                                "b": [
                                    1.11631076497947,
                                    3.15740674001365,
                                    1.93350786347877
                                ],
                                "c": [
                                    0,
                                    0,
                                    3.86701572695754
                                ]
                            }
                        }
                    }
                }
            ]
        """
        pass

    @abstractmethod
    def stress_tensor(self):
        """
        Returns stress tensor.

        Units: kbar

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

        Units: kbar

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

        Units: eV/angstrom

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

        Units: eV/angstrom

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
    def atomic_constraints(self):
        """
        Returns atomic constraints.

        Returns:
            list

        Example:
            [
                [
                    True,
                    False,
                    True
                ],
                [
                    False,
                    False,
                    True
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

        Units: angstrom^3

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

        Units: g/cm^3

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

        Units: eV

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

    @abstractmethod
    def magnetic_moments(self):
        """
        Returns magnetic moments.

        Units: uB

        Returns:
            list

        Examples:
             [[0, 0, 3.046], [0, 0, -3.045]]
        """
        pass
