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

        Returns:
            dict

        Example:
            [
                {
                    'element': 'C',
                    'electronicState': 's-down',
                    'value': [0.00015, 0.000187, 0.000232, 0.000287, 0.000355, 0.000437]
                },
                {
                    'element': 'Ti',
                    'electronicState': 'p-up',
                    'value': [6.87e-06, 8.5e-06, 1.0e-05, 1.3e-05, 1.63e-05, 2.01e-05]
                }
            ]
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
