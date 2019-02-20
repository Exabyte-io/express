import numpy as np
import pymatgen as mg

from abc import abstractmethod


class ElectronicDataMixin(object):
    """
    Defines electronic interfaces.

    Note:
        THE FORMAT OF DATA STRUCTURE RETURNED MUST BE PRESERVED IN IMPLEMENTATION.
    """

    @abstractmethod
    def total_energy(self):
        """
        Returns total energy.

        Units: eV

        Returns:
             float

        Example:
             -19.00890332
        """
        pass

    @abstractmethod
    def fermi_energy(self):
        """
        Returns fermi energy.

        Units: eV

        Returns:
             float

        Example:
             6.6078556811104292
        """
        pass

    @abstractmethod
    def nspins(self):
        """
        Returns the number of spins.

        Returns:
             int

        Example:
             2
        """
        pass

    @abstractmethod
    def eigenvalues_at_kpoints(self):
        """
        Returns eigenvalues for all kpoints.

        Units:
            energy: eV
            kpoint coordinate: crystal

        Returns:
             list[dict]

        Example:
            [
                {
                    'kpoint': [-0.5, 0.5, 0.5],
                    'weight': 9.5238095E-002,
                    'eigenvalues': [
                        {
                            'energies': [-1.4498446E-001, ..., 4.6507387E-001],
                            'occupations': [1, ... , 0],
                            'spin': 0.5
                        }
                    ]
                },
                ...
            ]
        """
        pass

    @abstractmethod
    def dos(self):
        """
        Returns density of states.

        Units:
            energy: eV
            partial: eV
            total: eV

        Returns:
            dict

        Example:
            {
                "energy": [
                    -6.005000114440918,
                    -5.954999923706055,
                    -5.90500020980835
                ],
                "partial": [
                    [
                        1.6499999980444308E-17,
                        1.3080000562020133E-16,
                        7.899999954541818E-16
                    ]
                ],
                "partial_info": [
                    {
                        "electronicState": "2py",
                        "element": "Si"
                    },
                    {
                        "electronicState": "2px",
                        "element": "Si"
                    },
                    {
                        "electronicState": "1s",
                        "element": "Si"
                    },
                    {
                        "electronicState": "2pz",
                        "element": "Si"
                    }
                ],
                "total": [
                    0.00012799999967683107,
                    0.0010100000072270632,
                    0.006130000110715628
                ]
            }
        """
        pass

    @abstractmethod
    def convergence_electronic(self):
        """
        Extracts convergence electronic.

        Returns:
             list[float]

        Example:
            [
                1.4018213061907816,
                0.5939946985677435,
                0.007003124785903934,
                0.0010198831091687887,
                4.2041606287774244e-05,
                7.619190783544846e-06
            ]
        """
        pass

    @abstractmethod
    def total_energy_contributions(self):
        """
        Extracts total energy contributions.

        Units:
            energy: eV

        Returns:
            dict

        Example:
            {
                "harrisFoulkes": {
                    "name": "harris_foulkes",
                    "value": -258.6293887585482
                },
                "ewald": {
                    "name": "ewald",
                    "value": -226.94126871332813
                },
                "oneElectron": {
                    "name": "one_electron",
                    "value": 68.65366986552296
                },
                "smearing": {
                    "name": "smearing",
                    "value": -0.0
                },
                "hartree": {
                    "name": "hartree",
                    "value": 17.72349166363712
                },
                "exchangeCorrelation": {
                    "name": "exchange_correlation",
                    "value": -118.06528742483022
                }
            }
        }
        """
        pass

    @abstractmethod
    def reaction_energies(self):
        """
        Returns reaction energies.

        Units: eV

        Returns:
             list[float]

        Example:
             [
                0.0000000000
                0.0336646452
                0.1282974628
                0.2032892090
                0.1282940160
                0.0336634943
                0.0000000063
            ]
        """
        pass

    @abstractmethod
    def reaction_coordinates(self):
        """
        Returns reaction coordinates.

        Returns:
             list[float]

        Example:
             [
                0.0000000000
                0.1932752934
                0.3596145525
                0.5000030773
                0.6403901111
                0.8067278352
                1.0000000000
            ]
        """
        pass

    def reaction_coordinates_from_poscars(self, poscars):
        """
        Returns reaction coordinates based on the given poscars.

        See `NEBAnalysis` class in http://pymatgen.org/_modules/pymatgen/analysis/transition_state.html for more info.

        Args:
            poscars (list): structures in POSCAR format.

        Returns:
             list
        """
        structures = [mg.Structure.from_str(poscar, "poscar") for poscar in poscars]
        prev = structures[0]
        reaction_coordinates = [0]
        for structure in structures[1:]:
            dists = np.array([s2.distance(s1) for s1, s2 in zip(prev, structure)])
            reaction_coordinates.append(np.sqrt(np.sum(dists ** 2)))
            prev = structure
        reaction_coordinates = np.cumsum(reaction_coordinates)
        return ((1 / reaction_coordinates[-1]) * reaction_coordinates).tolist()
