import numpy as np

from src.utils import find_file
from src.settings import Constant
from express.parsers.apps import BaseParser
from express.parsers.apps.espresso import settings
from express.parsers.mixins.ionic import IonicDataMixin
from express.parsers.mixins.reciprocal import ReciprocalDataMixin
from express.parsers.mixins.electronic import ElectronicDataMixin
from express.parsers.apps.espresso.formats.txt import EspressoTXTParser
from express.parsers.apps.espresso.formats.xml import EspressoXMLParser


class EspressoParser(BaseParser, IonicDataMixin, ElectronicDataMixin, ReciprocalDataMixin):
    """
    Espresso parser class.

    Args:
        work_dir (str): working directory path.
        kwargs (dict):
            app_stdout (str): path to the application stdout file.
    """

    def __init__(self, work_dir, **kwargs):
        super(EspressoParser, self).__init__(work_dir, **kwargs)
        self.txt_parser = EspressoTXTParser(self.work_dir)
        self.xml_parser = EspressoXMLParser(find_file(settings.XML_DATA_FILE, self.work_dir))

    def total_energy(self):
        """
        Returns total energy.

        Returns:
             float

        Example:
             -19.00890332
        """
        return self.txt_parser.total_energy(self._get_stdout_content())

    def fermi_energy(self):
        """
        Returns fermi energy.

        Returns:
             float

        Example:
             6.6078556811104292
        """
        return self.xml_parser.fermi_energy()

    def nspins(self):
        """
        Returns the number of spins.

        Returns:
             int

        Example:
             2
        """
        return self.xml_parser.nspins()

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
        eigenvalues_at_kpoints = self.xml_parser.eigenvalues_at_kpoints()
        for eigenvalues_at_kpoint in eigenvalues_at_kpoints:
            for eigenvalue in eigenvalues_at_kpoint["eigenvalues"]:
                eigenvalue['energies'] = np.array(eigenvalue['energies']) * Constant.HARTREE
        return eigenvalues_at_kpoints

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
        return self.xml_parser.ibz_k_points()

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
        return self.txt_parser.dos()

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
        return self.xml_parser.basis()

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
        return self.xml_parser.lattice(reciprocal=False)

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
        return self.txt_parser.convergence_electronic(self._get_stdout_content())

    def convergence_ionic(self):
        """
        Returns convergence ionic.

        Returns:
             list[dict]
        """
        return self.txt_parser.convergence_ionic(self._get_stdout_content())

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
        return self.txt_parser.stress_tensor(self._get_stdout_content())

    def pressure(self):
        """
        Returns pressure.

        Returns:
            float

        Examples:
             73.72
        """
        return self.txt_parser.pressure(self._get_stdout_content())

    def total_force(self):
        """
        Returns total force.

        Returns:
            float

        Example:
            1e-06
        """
        return self.txt_parser.total_force(self._get_stdout_content())

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
        return self.txt_parser.atomic_forces(self._get_stdout_content())

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
        return self.txt_parser.total_energy_contributions(self._get_stdout_content())
