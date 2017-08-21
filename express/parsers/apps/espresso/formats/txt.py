import os
import re
import StringIO
import numpy as np

from express.parsers.utils import find_file
from express.parsers.settings import Constant
from express.parsers.apps.espresso import settings
from express.parsers.formats.txt import BaseTXTParser

ORBITS = {
    's': [''],
    'p': ['z', 'x', 'y'],
    'd': ['z2', 'zx', 'zy', 'x2-y2', 'xy']
}


class EspressoTXTParser(BaseTXTParser):
    """
    Espresso text parser class.
    """

    def __init__(self, work_dir):
        super(EspressoTXTParser, self).__init__(work_dir)

    def total_energy(self, text):
        """
        Extracts total energy.

        Args:
            text (str): text to extract data from.

        Returns:
             float
        """
        return self._general_output_parser(text, **settings.REGEX["total_energy"])

    def dos(self):
        """
        Extracts density of states. It reads 'pdos_tot' file to extract energy levels and total DOS values for each
        energy level. Then it reads partial DOS files created by QE with this format: `__prefix__.pdos_atm#1(
        C)_wfc#1(s)` in job working directory. DOS value for each atom with the same element and orbit number will be
        added together and packed in a dictionary. The result containing energy levels, total DOS and partial DOS for
        each element will be returned.

        Returns:
            dict

        Example:
            {
                'energy': [-1.0, 0, 1.0],
                'total': [0.013, 0.124, 0.923],
                'partial': [
                    {
                        'element': 'C',
                        'electronicState': '1s',
                        'value': [0.00015, 0.000187, 0.000232, 0.000287, 0.000355, 0.000437]
                    },
                    {
                        'element': 'C',
                        'electronicState': '3px',
                        'value': [6.87e-06, 8.5e-06, 1.0e-05, 1.3e-05, 1.63e-05, 2.01e-05]
                    },
                ]
            }
        """
        dos_tot_file = find_file(settings.PDOS_TOT_FILE, self.work_dir)
        energy_levels, total_dos = self._total_dos(dos_tot_file)
        partial_dos_values, partial_dos_infos = self._partial_dos(len(energy_levels))
        return {
            'energy': energy_levels.tolist(),
            'total': total_dos.tolist(),
            'partial': partial_dos_values,
            'partial_info': partial_dos_infos
        }

    def _total_dos(self, dos_tot_file):
        """
        Parses total DOS from the given file. It reads the file to get energy levels and total DOS values for each
        energy level by extracting the first two columns.

        Example file:
            #
             E (eV)  dos(E)    pdos(E)
            -25.226  0.512E-03  0.504E-03
            -25.216  0.637E-03  0.628E-03
            -25.206  0.791E-03  0.779E-03

        Args:
            dos_tot_file (str): path to the pdos_tot file.

        Returns:
            tuple: energy levels and DOS total values.
                   Example:
                       ([-25.226, -25.216, -25.206], [0.512E-03, 0.637E-03, 0.791E-03])
        """
        if os.path.isfile(dos_tot_file):
            trimmed_dos_file = StringIO.StringIO(self._trim_dos_file(dos_tot_file))
            dos_tot = np.genfromtxt(trimmed_dos_file, dtype=np.float32, usecols=(0, 1))
            energy_levels = dos_tot[:, 0]
            dos_tot = dos_tot[:, 1]
            return energy_levels, dos_tot

    def _partial_dos(self, num_levels):
        """
        Parses partial DOS for each element with its orbit value. it reads partial DOS files created by QE with this
        format: `__prefix__.pdos_atm#1(C)_wfc#1(s)` in job working directory. DOS value for each atom with the same
        element and orbit number will be added together and packed in a dictionary.

        Args:
            num_levels (int): number of energy levels.

        Returns:
            dict: a dictionary containing partial DOS values for each element.
                Example:
                    [
                        {
                            'element': 'C',
                            'electronicState': '1s',
                            'value': [0.00015, 0.000187, 0.000232, 0.000287, 0.000355, 0.000437]
                        },
                        {
                            'element': 'C',
                            'electronicState': '3px',
                            'value': [6.87e-06, 8.5e-06, 1.0e-05, 1.3e-05, 1.63e-05, 2.01e-05]
                        }
                    ]
        """
        pdos = {}
        for file_name in os.listdir(self.work_dir):
            file_path = os.path.join(self.work_dir, file_name)
            match = re.compile(settings.REGEX['pdos_file']['regex']).match(file_name)
            if match:
                atm_pdos = self._extract_partial_dos(file_path, len(ORBITS[match.group('orbit_symbol')]))
                atm_pdos = atm_pdos.T if atm_pdos.shape[0] > 1 else atm_pdos
                for idx, orbit_pdos in enumerate(atm_pdos):
                    orbit_idx = ORBITS[match.group('orbit_symbol')][idx] if match.group('orbit_symbol') != 's' else ''
                    pdos_id = "{0}_{1}{2}{3}".format(match.group('atom_name'), match.group('orbit_num'),
                                                     match.group('orbit_symbol'), orbit_idx)  # e.g. C_1s, C_2px, C_2dz2
                    if not pdos_id in pdos.keys():
                        pdos[pdos_id] = np.zeros(num_levels)
                    pdos[pdos_id] += orbit_pdos

        pdos_values = [pdos[item].tolist() for item in pdos]
        pdos_infos = [{'element': item.split('_')[0], 'electronicState': item.split('_')[1]} for item in pdos]
        return pdos_values, pdos_infos

    def _extract_partial_dos(self, pdos_file, orbit_num):
        """
        Parses partial DOS values from a given file.

        Args:
            pdos_file (str): path to pdos file.

        Returns:
            numpy.ndarray
        """
        if os.path.isfile(pdos_file):
            trimmed_pdos_file = StringIO.StringIO(self._trim_dos_file(pdos_file))
            target_columns = range(2, 2 + orbit_num)
            columns = np.genfromtxt(trimmed_pdos_file, dtype=np.float32, usecols=range(2, 2 + orbit_num))
            return columns if len(target_columns) > 1 else np.array([columns])

    def _trim_dos_file(self, dos_file):
        """
        Trims a given dos file and returns the data. Only lines which start with a scientific number are interested.

        Args:
            dos_file (str): path to the dos file.

        Returns:
            (str): trimmed out text containing actual dos values.
                Example Input:
                    *******  0.000E+00  0.000E+00
                    *******  0.000E+00  0.000E+00
                    -99.989  0.000E+00  0.000E+00
                     99.939  0.000E+00  0.000E+00
                      9.889  0.000E+00  0.000E+00
                    *******  0.000E+00  0.000E+00
                    *******  0.000E+00  0.000E+00
                Example output:
                    -99.989  0.000E+00  0.000E+00
                    -99.939  0.000E+00  0.000E+00
                    -99.889  0.000E+00  0.000E+00
        """
        with open(dos_file) as f:
            return '\n'.join(re.findall('^ *[-+]?\d*\.\d+(?:[eE][-+]?\d+)?.*$', f.read(), re.MULTILINE))

    def convergence_electronic(self, text):
        """
        Extracts convergence electronic.

        Args:
            text (str): text to extract data from.

        Returns:
             list[float]
        """
        return np.array(
            self._general_output_parser(text, **settings.REGEX["convergence_electronic"])) * Constant.RYDBERG

    def convergence_ionic(self, text):
        """
        Extracts convergence ionic.

        Args:
            text (str): text to extract data from.

        Returns:
             list[dict]
        """
        energies = (
        np.array(self._general_output_parser(text, **settings.REGEX["convergence_ionic"])) * Constant.RYDBERG).tolist()
        lattice_convergence = self._lattice_convergence(text)
        basis_convergence = self._basis_convergence(text)
        if energies:
            data = [{'energy': _} for _ in energies]
            for idx, structure in enumerate(zip(lattice_convergence, basis_convergence)):
                data[idx].update({'structure': {
                    'lattice': structure[0],
                    'basis': structure[1]
                }})
            return data

    def _lattice_convergence(self, text):
        """
        Extracts lattice convergence values computed in each BFGS step.

        Args:
            text (str): text to extract data from.

        Returns:
            list

        Example:
            [
                {
                    'vectors': {
                        'a': [-0.561154473, -0.000000000, 0.561154473],
                        'b': [-0.000000000, 0.561154473, 0.561154473],
                        'c': [-0.561154473, 0.561154473, 0.000000000],
                        'alat': 9.44858082
                    }
                 },
                ...
                {
                    'vectors': {
                        'a': [-0.561154473, -0.000000000, 0.561154473],
                        'b': [-0.000000000, 0.561154473, 0.561154473],
                        'c': [-0.561154473, 0.561154473, 0.000000000],
                        'alat': 9.44858082
                    }
                 }
             ]
        """
        return self._extract_data_from_bfgs_blocks(text, self._extract_lattice)

    def _extract_data_from_bfgs_blocks(self, text, func):
        """
        Extracts data from BFGS blocks using the provided function.

        Args:
            text (str): text to extract data from.
            func (func): function object to be applied on the content block.

        Returns:
            list: list of information extracted using the provided function
        """
        results = []
        bfgs_block_pattern = re.compile(settings.REGEX["bfgs_block"]["regex"], re.DOTALL)
        bfgs_blocks = bfgs_block_pattern.findall(text)
        for block in bfgs_blocks:
            results.append(func(block))
        return results

    def _extract_lattice(self, text, last_value=False):
        """
        Extracts lattice.

        Args:
            text (str): text to extract data from.

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
        text = text[text.find('Begin final coordinates'):] if last_value else text
        match = re.search(settings.REGEX["lattice"], text)
        if match:
            lattice = [float(_) for _ in match.groups(1)]
            return {
                'vectors': {
                    'a': lattice[1:4],
                    'b': lattice[4:7],
                    'c': lattice[7:10],
                    'alat': lattice[0]
                }
            }

    def _basis_convergence(self, text):
        """
        Extracts convergence bases computed in each BFGS step.

        Args:
            text (str): text to extract data from.

        Returns:
            list

        Example:
            [
                {
                    'units': 'crystal',
                    'elements': [{'id': 1, 'value': 'Si'}, {'id': 2, 'value': 'Si'}],
                    'coordinates': [{'id': 1, 'value': [0.0, 0.0, 0.0]}, {'id': 2, 'value': [0.0, 0.0, 0.0]}]
                 },
                ...
                {
                    'units': 'crystal',
                    'elements': [{'id': 1, 'value': 'Si'}, {'id': 2, 'value': 'Si'}],
                    'coordinates': [{'id': 1, 'value': [0.0, 0.0, 0.0]}, {'id': 2, 'value': [0.0, 0.0, 0.0]}]
                 }
            ]
        """
        return self._extract_data_from_bfgs_blocks(text, self._extract_basis)

    def _extract_basis(self, text, last_value=False):
        """
        Extracts basis data.

        Args:
            text (str): text to extract data from.

        Returns:
            dict

        Example:
            {
                'units': 'crystal',
                'elements': [{'id': 1, 'value': 'Si'}, {'id': 2, 'value': 'Si'}],
                'coordinates': [{'id': 1, 'value': [0.0, 0.0, 0.0]}, {'id': 2, 'value': [0.0, 0.0, 0.0]}]
             }
        """
        text = text[text.find('Begin final coordinates'):] if last_value else text
        basis = {
            'units': 'crystal',
            'elements': [],
            'coordinates': []
        }

        matches = re.findall(settings.REGEX["ion_position"], text)
        if matches:
            for idx, match in enumerate(matches):
                basis['elements'].append({
                    'id': idx,
                    'value': match[0]
                })
                basis['coordinates'].append({
                    'id': idx,
                    'value': [float(match[1]), float(match[2]), float(match[3])]
                })

            return basis

    def stress_tensor(self, text):
        """
        Extracts stress tensor.

        Args:
            text (str): text to extract data from.

        Returns:
            list
        """
        return self._general_output_parser(text, **settings.REGEX["stress_tensor"])

    def pressure(self, text):
        """
        Extracts pressure.

        Args:
            text (str): text to extract data from.

        Returns:
            float
        """
        return self._general_output_parser(text, **settings.REGEX["pressure"])

    def total_force(self, text):
        """
        Extracts total force.

        Returns:
            float
        """
        return self._general_output_parser(text, **settings.REGEX["total_force"])

    def atomic_forces(self, text):
        """
        Extracts atomic forces.

        Args:
            text (str): text to extract data from.

        Returns:
            list
        """
        return self._general_output_parser(text, **settings.REGEX['forces_on_atoms'])

    def total_energy_contributions(self, text):
        """
        Extracts total energy contributions.

        Args:
            text (str): text to extract data from.

        Returns:
            dict
        """
        energy_contributions = {}
        for contribution in settings.TOTAL_ENERGY_CONTRIBUTIONS:
            value = self._general_output_parser(text, **settings.TOTAL_ENERGY_CONTRIBUTIONS[contribution])
            if value is not None:
                energy_contributions.update({contribution: {
                    'name': contribution,
                    'value': value * Constant.RYDBERG
                }})
        return energy_contributions

    def zero_point_energy(self, text):
        """
        Extracts zero point energy.

        Returns:
             float
        """
        data = self._general_output_parser(text, **settings.REGEX['zero_point_energy'])
        return (sum(data) / 2) * Constant.cm_inv_to_ev
