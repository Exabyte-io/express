import os
import re
import io
import numpy as np
from pathlib import Path
from typing import Dict, Optional

from express.parsers.utils import find_file
from express.parsers.settings import Constant, GENERAL_REGEX, ATOMIC_REGEX
from express.parsers.apps.espresso import settings
from express.parsers.formats.txt import BaseTXTParser

ORBITS = {"s": [""], "p": ["z", "x", "y"], "d": ["z2", "zx", "zy", "x2-y2", "xy"]}


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
        return Constant.RYDBERG * self._general_output_parser(text, **settings.REGEX["total_energy"])

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
            "energy": energy_levels.tolist(),
            "total": total_dos.tolist(),
            "partial": partial_dos_values,
            "partial_info": partial_dos_infos,
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
            trimmed_dos_file = io.StringIO(self._trim_dos_file(dos_tot_file))
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
        # Because os.listdir() has an undefined order specified, we'll sort the file list in order to have a
        # reproducible result.  The sort order will be the normal alphanumeric comparison.
        # For example:
        # >>> x = ['a', 'B', 'c', 'D']
        # >>> sorted(x)
        # ['B', 'D', 'a', 'c']
        for file_name in sorted(os.listdir(self.work_dir)):
            file_path = os.path.join(self.work_dir, file_name)
            match = re.compile(settings.REGEX["pdos_file"]["regex"]).match(file_name)
            if match:
                atm_pdos = self._extract_partial_dos(file_path, len(ORBITS[match.group("orbit_symbol")]))
                atm_pdos = atm_pdos.T if atm_pdos.shape[0] > 1 else atm_pdos
                for idx, orbit_pdos in enumerate(atm_pdos):
                    orbit_idx = ORBITS[match.group("orbit_symbol")][idx] if match.group("orbit_symbol") != "s" else ""
                    pdos_id = "{0}_{1}{2}{3}".format(
                        match.group("atom_name"), match.group("orbit_num"), match.group("orbit_symbol"), orbit_idx
                    )  # e.g. C_1s, C_2px, C_2dz2
                    if pdos_id not in pdos.keys():
                        pdos[pdos_id] = np.zeros(num_levels)
                    pdos[pdos_id] += orbit_pdos

        pdos_values = [pdos[item].tolist() for item in pdos]
        pdos_infos = [{"element": item.split("_")[0], "electronicState": item.split("_")[1]} for item in pdos]
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
            trimmed_pdos_file = io.StringIO(self._trim_dos_file(pdos_file))
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
            return "\n".join(re.findall("^ *[-+]?\d*\.\d+(?:[eE][-+]?\d+)?.*$", f.read(), re.MULTILINE))

    def convergence_electronic(self, text):
        """
        Extracts convergence electronic.

        Args:
            text (str): text to extract data from.

        Returns:
             list[float]
        """
        data = self._general_output_parser(text, **settings.REGEX["convergence_electronic"])
        # The next 3 lines are necessary to have realtime data
        ionic_data = [_["electronic"]["data"] for _ in self.convergence_ionic(text)]
        last_step_data = data[sum([len(_) for _ in ionic_data]) : len(data)]
        if last_step_data:
            ionic_data.append(last_step_data)
        return [(np.array(_) * Constant.RYDBERG).tolist() for _ in ionic_data]

    def convergence_ionic(self, text):
        """
        Extracts convergence ionic.

        Args:
            text (str): text to extract data from.

        Returns:
             list[dict]
        """
        data = []
        blocks = re.findall(settings.REGEX["convergence_ionic_blocks"]["regex"], text, re.DOTALL | re.MULTILINE)
        for idx, block in enumerate(blocks):
            energies = self._general_output_parser(block, **settings.REGEX["convergence_ionic_energies"])
            energies = (np.array(energies) * Constant.RYDBERG).tolist()
            data.append(
                {
                    "energy": energies[-1],
                    "electronic": {
                        "units": "eV",
                        "data": self._general_output_parser(block, **settings.REGEX["convergence_electronic"]),
                    },
                }
            )

        if not data:
            return []

        # last structure is used for the next ionic step, hence [:max(0, len(data) - 1)]
        lattice_convergence = self._lattice_convergence(text)[: max(0, len(data) - 1)]
        basis_convergence = self._basis_convergence(text)[: max(0, len(data) - 1)]
        for idx, structure in enumerate(zip(lattice_convergence, basis_convergence)):
            structure[1]["units"] = "angstrom"
            lattice_matrix = np.array([structure[0]["vectors"][key] for key in ["a", "b", "c"]]).reshape((3, 3))
            for coordinate in structure[1]["coordinates"]:
                coordinate["value"] = np.dot(coordinate["value"], lattice_matrix).tolist()
            data[idx + 1].update({"structure": {"lattice": structure[0], "basis": structure[1]}})

        # inject initial structure
        data[0].update(
            {"structure": {"basis": self.initial_basis(text), "lattice": self.initial_lattice_vectors(text)}}
        )

        return data

    def initial_lattice_vectors(self, text):
        """
        Extracts initial lattice from a given text.

        Note: The initial lattice is in alat format and hence it needs to be converted to angstrom.

        The text looks like the following:

            crystal axes: (cart. coord. in units of alat)
               a(1) = (   0.866025   0.000000   0.500000 )
               a(2) = (   0.288675   0.816497   0.500000 )
               a(3) = (   0.000000   0.000000   1.000000 )

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
                    'alat': 1
                }
            }
        """
        alat = self._get_alat(text)
        lattice_in_alat_units = self._extract_lattice(text, regex="lattice_alat")
        for key in ["a", "b", "c"]:
            lattice_in_alat_units["vectors"][key] = [
                e * alat * Constant.BOHR for e in lattice_in_alat_units["vectors"][key]
            ]
        return lattice_in_alat_units

    def _extract_basis(self, text, number_of_atoms):
        """
        Extracts the basis from the given text.

        Note: no units conversion is done in here.

        """
        basis = {"units": "angstrom", "elements": [], "coordinates": []}
        matches = self._general_output_parser(text, **settings.REGEX["basis_alat"](number_of_atoms))
        for idx, match in enumerate(matches):
            basis["elements"].append({"id": idx, "value": match[0]})
            coordinate = [float(match[1]), float(match[2]), float(match[3])]
            basis["coordinates"].append({"id": idx, "value": coordinate})
        return basis

    def _get_alat(self, text):
        return self._general_output_parser(text, **settings.REGEX["lattice_parameter_alat"])[0]

    def _number_of_atoms(self, text):
        return self._general_output_parser(text, **settings.REGEX["number_of_atoms"])[0]

    def initial_basis(self, text):
        """
        Extracts initial basis from a given text.

        Units: angstrom

        The text looks like the following:

             site n.     atom                  positions (alat units)
                 1           Si  tau(   1) = (   0.0000000   0.0000000   0.0000000  )
                 2           Si  tau(   2) = (   0.2886752   0.2041241   0.5000000  )

        Args:
            text (str): text to extract data from.

        Returns:
            dict

         Example:
            {
                'units': 'angstrom',
                'elements': [{'id': 1, 'value': 'Si'}, {'id': 2, 'value': 'Si'}],
                'coordinates': [{'id': 1, 'value': [0.0, 0.0, 0.0]}, {'id': 2, 'value': [2.1095228, 1.49165, 3.6538]}]
             }
        """
        alat = self._get_alat(text)
        number_of_atoms = self._number_of_atoms(text)
        basis_in_alat_units = self._extract_basis(text[text.find("positions (alat units)") :], number_of_atoms)
        for coordinate in basis_in_alat_units["coordinates"]:
            coordinate["value"] = [x * alat * Constant.BOHR for x in coordinate["value"]]
        return basis_in_alat_units

    def _lattice_convergence(self, text):
        """
        Extracts lattice convergence values in angstrom units computed in each BFGS step.

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
                        'alat': 1
                    }
                 },
                ...
                {
                    'vectors': {
                        'a': [-0.561154473, -0.000000000, 0.561154473],
                        'b': [-0.000000000, 0.561154473, 0.561154473],
                        'c': [-0.561154473, 0.561154473, 0.000000000],
                        'alat': 1
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

    def _extract_lattice(self, text, regex="lattice"):
        """
        Extracts lattice.

        Note: no units conversion is done in here.

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
                    'alat': 1
                }
            }
        """
        match = re.search(settings.REGEX[regex]["regex"], text)
        if match:
            lattice = [float(_) for _ in match.groups(1)]
            return {"vectors": {"a": lattice[0:3], "b": lattice[3:6], "c": lattice[6:9], "alat": 1}}

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
        return self._extract_data_from_bfgs_blocks(text, self._extract_basis_from_bfgs_blocks)

    def _extract_basis_from_bfgs_blocks(self, text):
        """
        Extracts basis data in crystal units.

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
        basis = {"units": "crystal", "elements": [], "coordinates": []}
        matches = re.findall(settings.REGEX["ion_position"]["regex"], text)
        if matches:
            for idx, match in enumerate(matches):
                basis["elements"].append({"id": idx, "value": match[0]})
                basis["coordinates"].append({"id": idx, "value": [float(match[1]), float(match[2]), float(match[3])]})

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
        return self._general_output_parser(text, **settings.REGEX["total_force"]) * Constant.ry_bohr_to_eV_A

    def atomic_forces(self, text):
        """
        Extracts atomic forces.

        Args:
            text (str): text to extract data from.

        Returns:
            list
        """
        forces = self._general_output_parser(text, **settings.REGEX["forces_on_atoms"])
        return (np.array(forces) * Constant.ry_bohr_to_eV_A).tolist()

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
                energy_contributions.update({contribution: {"name": contribution, "value": value * Constant.RYDBERG}})
        return energy_contributions

    def zero_point_energy(self, text):
        """
        Extracts zero point energy.

        Returns:
             float
        """
        data = self._general_output_parser(text, **settings.REGEX["zero_point_energy"])
        if len(data):
            return (sum(data) / 2) * Constant.cm_inv_to_ev

    def phonon_dos(self):
        """
        Extract vibrational frequencies and total DOS.

        Returns:
            dict

        Example:
            {
                'frequency': [-1.2588E-05, 9.9999E-01, 2.0000E+00, 3.0000E+00, ....]
                'total': [0.0000E+00, 2.5386E-07, 1.0154E-06, 2.2847E-06, ....]
            }
        """
        phonon_dos_tot_file = find_file(settings.PHONON_DOS_FILE, self.work_dir)
        frequencies, total_phonon_dos = self._total_dos(phonon_dos_tot_file)
        return {"frequency": frequencies.tolist(), "total": total_phonon_dos.tolist()}

    def phonon_dispersions(self):
        """
        Extract vibrational frequencies at qpoints along the high symmetry points in Brillouin zone.

        Returns:
            dict

        Example:
            {
                'qpoints': [[0.00, 0.00, 0.00],[0.00, 0.00, 0.01],....],
                'frequencies': [['-0.0000', '-0.0000', '-0.0000', '574.0778', '574.0778', '574.2923'],
                ['29.3716', '30.0630', '70.4699', '568.0790', '569.7664', '569.9710'], ....]
            }
        """
        modes_file = find_file(settings.PHONON_MODES_FILE, self.work_dir)
        qpoints, frequencies = self.phonon_frequencies(modes_file)
        return {"qpoints": qpoints.tolist(), "frequencies": frequencies.tolist()}

    def phonon_frequencies(self, modes_file):
        """
        Extracts qpoints along the paths in Brillouin zone and the phonon frequencies at each qpoint.

        Example file:
            #
             q =       0.0000      0.0000      0.0000
             **************************************************************************
             freq (    1) =      -0.004399 [THz] =      -0.146739 [cm-1]
             ( -0.366864   0.000000     0.211786   0.000000     0.265747   0.000000   )
             ( -0.367203   0.000000     0.211982   0.000000     0.264868   0.000000   )
             ( -0.367036   0.000000     0.211885   0.000000     0.265493   0.000000   )
             ( -0.367206   0.000000     0.211984   0.000000     0.264823   0.000000   )
             freq (    2) =      -0.004372 [THz] =      -0.145845 [cm-1]
             ....
             ....
             **************************************************************************
             q =       0.0000      0.0000      0.1000
             **************************************************************************
             freq (    1) =      -0.004399 [THz] =      -0.146739 [cm-1]
             ( -0.366864   0.000000     0.211786   0.000000     0.265747   0.000000   )
             ( -0.367203   0.000000     0.211982   0.000000     0.264868   0.000000   )
             ( -0.367036   0.000000     0.211885   0.000000     0.265493   0.000000   )
             ( -0.367206   0.000000     0.211984   0.000000     0.264823   0.000000   )
             freq (    2) =      -0.004372 [THz] =      -0.145845 [cm-1]
             ....
             ....
             **************************************************************************

        Args:
            modes_file (str): path to modes file (normal_modes.out).

        Returns:
            tuple

        Example:
            ([
                [0.0000, 0.0000, 0.0000],
                [0.000, 0.0000, 0.1000]
            ],
            [
                [5.7429E+02, 5.7429E+02],
                [5.69970E+02, 5.69970E+02],
                .....,
                [4.5469E+02, 4.5469E+02]
            ])
        """
        with open(modes_file, "r") as f:
            text = f.read()
        qpoints = np.array(re.compile(settings.REGEX["qpoints"]["regex"]).findall(text), dtype=np.float32)
        frequencies = np.array(
            re.compile(settings.REGEX["phonon_frequencies"]["regex"]).findall(text), dtype=np.float32
        )
        frequencies = np.transpose(frequencies.reshape(qpoints.shape[0], frequencies.shape[0] // qpoints.shape[0]))
        return qpoints, frequencies

    def reaction_coordinates(self, text):
        """
        Extracts reaction coordinates from the first column of NEB dat file.

        Example input:
            0.0000000000      0.0000000000      0.1145416373
            0.1944842569      0.0341286086      0.0886712471
            0.3625057164      0.1308566687      0.0995133799
            0.4999390812      0.2030519699      0.0010169552
            0.6383139128      0.1302022095      0.0385626296
            0.8046562342      0.0345676488      0.0062796586
            1.0000000000      0.0000000063      0.1146893883


        Returns:
            list[float]
        """
        return self._general_output_parser(text, **settings.REGEX["reaction_coordinates"])

    def reaction_energies(self, text):
        """
        Extracts reaction energies from the second column of NEB dat file.

        Example input:
            0.0000000000      0.0000000000      0.1145416373
            0.1944842569      0.0341286086      0.0886712471
            0.3625057164      0.1308566687      0.0995133799
            0.4999390812      0.2030519699      0.0010169552
            0.6383139128      0.1302022095      0.0385626296
            0.8046562342      0.0345676488      0.0062796586
            1.0000000000      0.0000000063      0.1146893883


        Returns:
            list[float]
        """
        return self._general_output_parser(text, **settings.REGEX["reaction_energies"])

    def potential_profile(self, text):
        """
        Extracts potential (hartree, local, hartree+local) along z.

        Example input:
            #z (A)  Tot chg (e/A)  Avg v_hartree (eV)  Avg v_local (eV)  Avg v_hart+v_loc (eV)
             -4.89        2.3697          -6.5847438         6.4872255        -0.0975183
             -4.78        2.1422          -7.0900648         8.2828137         1.1927490
             -4.67        2.0006          -7.5601238        10.1322914         2.5721676
             -4.56        1.8954          -7.9743444        11.9417738         3.9674294
             -4.44        1.7923          -8.3174980        13.6185904         5.3010924
             -4.33        1.6879          -8.5750414        15.0903496         6.5153082
             -4.22        1.5891          -8.7323531        16.2665057         7.5341527
             -4.11        1.5036          -8.7756094        17.0759068         8.3002974
             -4.00        1.4383          -8.6928512        17.5243394         8.8314882
             -3.89        1.3984          -8.4749404        17.6353196         9.1603792

        Returns:
            list[list[float]]
        """
        data = self._general_output_parser(text, **settings.REGEX["potential_profile"])
        return [[e[i] for e in data] for i in range(4)]

    def charge_density_profile(self, text):
        """
        Extracts total charge density along z.

        Example input:
            #z (A)  Tot chg (e/A)  Avg v_hartree (eV)  Avg v_local (eV)  Avg v_hart+v_loc (eV)
             -4.89        2.3697          -6.5847438         6.4872255        -0.0975183
             -4.78        2.1422          -7.0900648         8.2828137         1.1927490
             -4.67        2.0006          -7.5601238        10.1322914         2.5721676
             -4.56        1.8954          -7.9743444        11.9417738         3.9674294
             -4.44        1.7923          -8.3174980        13.6185904         5.3010924
             -4.33        1.6879          -8.5750414        15.0903496         6.5153082
             -4.22        1.5891          -8.7323531        16.2665057         7.5341527
             -4.11        1.5036          -8.7756094        17.0759068         8.3002974
             -4.00        1.4383          -8.6928512        17.5243394         8.8314882
             -3.89        1.3984          -8.4749404        17.6353196         9.1603792

        Returns:
            list[list[float]]
        """
        data = self._general_output_parser(text, **settings.REGEX["charge_density_profile"])
        return [[e[i] for e in data] for i in range(2)]

    def eigenvalues_at_kpoints_from_sternheimer_gw_stdout(self, text, inverse_reciprocal_lattice_vectors):
        """
        Extracts eigenvalues for all kpoints from Sternheimer GW stdout file.

        Example input:

            LDA eigenval (eV)   -5.60    6.25    6.25    6.25    8.69    8.69    8.69    9.37

            GWKpoint cart :   0.0000   0.0000   0.0000

            GWKpoint cryst:   0.0000   0.0000   0.0000
            GW qp energy (eV)   -7.08    5.34    5.34    5.34   10.15   10.15   10.15   10.82
            Vxc expt val (eV)  -10.09  -10.20  -10.20  -10.20   -9.85   -9.85   -9.85  -10.34
            Sigma_ex val (eV)  -16.04  -15.82  -15.82  -15.82   -3.54   -3.54   -3.54   -4.03
            QP renorm            1.00    1.00    1.00    1.00    1.00    1.00    1.00    1.00

        Returns:
            list[]
        """
        kpoints = self._general_output_parser(text, **settings.REGEX["sternheimer_gw_kpoint"])
        eigenvalues = self._general_output_parser(text, **settings.REGEX["sternheimer_gw_eigenvalues"])
        eigenvalues = [[float(x) for x in re.sub(" +", " ", e).strip(" ").split(" ")] for e in eigenvalues]
        return [
            {
                "kpoint": np.dot(point, inverse_reciprocal_lattice_vectors).tolist(),
                "weight": 1.0 / len(kpoints),  # uniformly set the weights as they are not extractable.
                "eigenvalues": [
                    {
                        "energies": eigenvalues[index],
                        "occupations": [],  # set occupations empty as they are not extractable.
                        "spin": 0.5,  # spin-polarized calculation is not supported yet, hence 0.5
                    }
                ],
            }
            for index, point in enumerate(kpoints)
        ]

    def final_basis(self, text):
        """
        Extracts final basis in angstrom units.
        """
        atomic_position_last_index = text.rfind("ATOMIC_POSITIONS (crystal)")
        if atomic_position_last_index < 0:
            return self.initial_basis(text)
        number_of_atoms = self._number_of_atoms(text)
        basis = self._extract_basis(text[atomic_position_last_index:], number_of_atoms)

        # final basis is in crystal units, hence it needs to be converted into angstrom.
        final_lattice_vectors = self.final_lattice_vectors(text)
        lattice_matrix = np.array([final_lattice_vectors["vectors"][key] for key in ["a", "b", "c"]]).reshape((3, 3))
        for coordinate in basis["coordinates"]:
            coordinate["value"] = np.dot(coordinate["value"], lattice_matrix).tolist()

        return basis

    def final_lattice_vectors(self, text):
        """
        Extracts final lattice in angstrom units.
        """
        cell_parameters_last_index = text.rfind("CELL_PARAMETERS (angstrom)")
        if cell_parameters_last_index < 0:
            return self.initial_lattice_vectors(text)
        return self._extract_lattice(text[cell_parameters_last_index:])

    def average_quantity(self, stdout_file: str) -> np.ndarray:
        """
        Extract planar and macroscopic averages of a quantity from the output of average.x (output file or avg.dat)
        The format is as follows:
        x  p(x)  m(x)
        whereby:
           x    = coordinate (a.u) along direction idir
                  x runs from 0 to the length of primitive vector idir
           p(x) = planar average, as defined above
           m(x) = macroscopic average, as defined above


        Example input:
             0.000000000    0.265457609    0.265456764
             0.017892431    0.265457604    0.265456756
             0.035784862    0.265457529    0.265456749
             0.053677293    0.265457391    0.265456743
             0.071569724    0.265457202    0.265456738
        """
        average_file = find_file(settings.AVERAGE_FILE, self.work_dir)
        # backup in case avg.dat doesn't exist
        if type(average_file) != str:
            average_file = find_file(stdout_file, self.work_dir)
        if type(average_file) == str and os.path.isfile(average_file):
            dtype = np.dtype([("x", float), ("planar_average", float), ("macroscopic_average", float)])
            data = np.fromregex(average_file, settings.REGEX["average_quantity"]["regex"], dtype)
            return data

    def dielectric_tensor_generic(self, dat_file: Path) -> Optional[np.ndarray]:
        """Extract the dielectric tensor (real or imaginary) produced by epsilon.x.

        Example input:
        # energy grid [eV]     epsr_x  epsr_y  epsr_z
        # plasmon frequences [eV]:    17.763649847   17.763705060   17.763291644
            0.000000000   20.137876673   20.137876704   20.137849785
            0.060120240   20.143821034   20.143821066   20.143794147
            0.120240481   20.161680126   20.161680158   20.161653237
            0.180360721   20.191532277   20.191532311   20.191505388

        Note:
            Values can be "NaN" which numpy interprets as np.nan. Hence the np.nan_to_num() call at the end.
        """
        data = None
        try:
            data = np.loadtxt(
                dat_file,
                dtype=np.dtype([("energy", float), ("eps", (float, 3))]),
                converters=lambda x: np.nan_to_num(float(x)),
            )
        except Exception as e:
            print(e)
        return data

    def parse_hubbard_u(self) -> Dict[str, list]:
        """
        Extract Hubbard parameters produced by hp.x

        filename: __prefix__.Hubbard_parameters.dat

        Example input content:
        =-------------------------------------------------------------------------------=

                                        Hubbard U parameters:

            site n.  type  label  spin  new_type  new_label  manifold  Hubbard U (eV)
                1        1    Co1     1      1         Co1        3d       6.7553
                2        2    Co2    -1      1         Co1        3d       6.7553

        =-------------------------------------------------------------------------------=

        returns list of following (example) data:
        {
            "values": [
                {
                "id": 1,
                "atomicSpecies": "Co1",
                "orbitalName": "3d",
                "value": 6.7553
                },
                {
                "id": 2,
                "atomicSpecies": "Co2",
                "orbitalName": "3d",
                "value": 6.7553
                }
            ]
        }
        """
        dat_file = find_file(settings.HP_FILE, self.work_dir)
        with open(dat_file, "r", encoding="utf-8") as fp:
            data = fp.read()

        RE_HP_HEADER = (r"\s*({0})\s*({1})\s+({2})\s+({3})\s+({4})\s+({5})\s+({6})\s+({7})\s+({8})\s*").format(
            "Hubbard U parameters:",
            "site n.",
            "type",
            "label",
            "spin",
            "new_type",
            "new_label",
            "manifold",
            "Hubbard U \(eV\)",
        )
        RE_HP_DATA = r"\s*{0}\s+{0}\s+{1}\s+{0}\s+{0}\s+{1}\s+{2}\s+{3}".format(
            GENERAL_REGEX["int_number"],
            ATOMIC_REGEX["atomicSpecies"],
            ATOMIC_REGEX["orbitalName"],
            GENERAL_REGEX["double_number"],
        )
        RE_HP_BLOCK = r"{0}({1})+".format(RE_HP_HEADER, RE_HP_DATA)

        try:
            hp_block = re.search(RE_HP_BLOCK, data, re.MULTILINE).group()
        except Exception:
            hp_block = ""

        hp_data = re.findall(r"^{0}".format(RE_HP_DATA), hp_block, re.MULTILINE)

        values = []

        for row in hp_data:
            cols = re.sub(r"([\s\t\r\n])+", " ", row.strip()).split(" ")
            values.append(
                {
                    "id": int(cols[0]),
                    "atomicSpecies": cols[2],
                    "newLabel": cols[5],
                    "orbitalName": cols[6],
                    "value": float(cols[7]),
                }
            )

        # let's return dictionary instead of bare values array, in future we
        # might decide to include more entities e.g., heder labels
        return {
            "values": values,
        }

    def parse_hubbard_v(self) -> Dict[str, list]:
        """
        Parse Hubbard V parameters produced by hp.x for all neighbors in 3⨉3⨉3
        supercell.

        filename: __prefix__.Hubbard_parameters.dat

        Example input content:

        =-------------------------------------------------------------------------------=
                           Hubbard V parameters:
                      (adapted for a supercell 3x3x3)

            Atom 1     Atom 2    Distance (Bohr)  Hubbard V (eV)

             1 Co1      1 Co1       0.000000        5.0634
             1 Co1     12 O         3.916149        0.2006
             1 Co1     20 O         3.916149        0.2006
             1 Co1     10 Co2       5.849456       -1.7819

             2 Co2      2 Co2       0.000000        5.6920
             2 Co2     48 O         3.916149        0.2100
             2 Co2     24 O         3.916149        0.2100
             2 Co2     57 Co1       5.849456       -1.7819

             3 O        3 O         0.000000        7.9678
             3 O       22 Co2       3.916149        0.2100
             3 O       57 Co1       3.916149        0.2006
             3 O       12 O         5.849456       -1.0886

             4 O        4 O         0.000000        7.9678
             4 O       58 Co2       3.916149        0.2100
             4 O       69 Co1       3.916149        0.2006
             4 O       59 O         5.849456       -1.0886
        =-------------------------------------------------------------------=

        returns list of following (example) data:
        {
            "values": [
                {
                    "id": 1,
                    "atomicSpecies": "Co1",
                    "orbitalName": "3d",
                    "id2": 1,
                    "atomicSpecies2": "Co1",
                    "orbitalName2": "3d",
                    "distance": 0.0,
                    "value": 5.0634
                },
                {
                    "id": 1,
                    "atomicSpecies": "Co1",
                    "orbitalName": "3d",
                    "id2": 12,
                    "atomicSpecies2": "O",
                    "orbitalName2": "2p",
                    "distance": 3.916149,
                    "value": 0.2006
                }
            ]
        }
        """
        dat_file = find_file(settings.HP_FILE, self.work_dir)
        with open(dat_file, "r", encoding="utf-8") as fp_v:
            data = fp_v.read()

        RE_HP_HEADER = (r"\s*({0})\s*({1})\s*({2})\s*({3})\s+({4})\s+({5})\s*").format(
            "Hubbard V parameters:",
            "\(adapted for a supercell 3x3x3\)",
            "Atom 1",
            "Atom 2",
            "Distance \(Bohr\)",
            "Hubbard V \(eV\)",
        )
        RE_HP_DATA = r"\s*{0}\s+{1}\s+{0}\s+{1}\s+{2}\s+{2}".format(
            GENERAL_REGEX["int_number"],
            ATOMIC_REGEX["atomicSpecies"],
            GENERAL_REGEX["double_number"],
        )

        RE_HP_BLOCK = r"{0}({1})+".format(RE_HP_HEADER, RE_HP_DATA)

        try:
            hp_block = re.search(RE_HP_BLOCK, data, re.MULTILINE).group()
        except Exception:
            hp_block = ""

        hp_data = re.findall(r"^{0}".format(RE_HP_DATA), hp_block, re.MULTILINE)

        # get orbitalName from atomicSpecies (new_label), find it from Hubbard U parser
        u_dict = self.parse_hubbard_u()["values"]
        values = []

        for row in hp_data:
            cols = re.sub(r"([\s\t\r\n])+", " ", row.strip()).split(" ")
            values.append(
                {
                    "id": int(cols[0]),
                    "atomicSpecies": cols[1],
                    "orbitalName": next(
                        (item["orbitalName"] for item in u_dict if item["newLabel"] == cols[1]), "nl"
                    ),
                    "id2": int(cols[2]),
                    "atomicSpecies2": cols[3],
                    "orbitalName2": next(
                        (item["orbitalName"] for item in u_dict if item["newLabel"] == cols[3]), "nl"
                    ),
                    "distance": float(cols[4]),
                    "value": float(cols[5]),
                }
            )

        return {
            "values": values,
        }

    def parse_hubbard_v_nn(self) -> Dict[str, list]:
        """
        Parse Hubbard V parameters produced by hp.x for 6 nearest neighbors.

        filename: HUBBARD.dat

        Example input content:

        # Copy this data in the pw.x input file for DFT+Hubbard calculations
        HUBBARD {ortho-atomic}
        V     Co-3d     Co-3d    1     1   7.7514
        V     Co-3d      O-2p    1    19   0.7573
        V     Co-3d      O-2p    1    46   0.7573
        V     Co-3d      O-2p    1    43   0.7573
        V     Co-3d      O-2p    1    54   0.7573
        V     Co-3d      O-2p    1    11   0.7573
        V     Co-3d      O-2p    1    22   0.7573

        returns list of following (example) data:

        {
            "values": [
                {
                "id": 1,
                "atomicSpecies": "Co",
                "orbitalName": "3d",
                "id2": 1,
                "atomicSpecies2": "Co",
                "orbitalName2": "3d",
                "value": 7.7514
                },
                {
                "id": 1,
                "atomicSpecies": "Co",
                "orbitalName": "3d",
                "id2": 19,
                "atomicSpecies2": "O",
                "orbitalName2": "2p",
                "value": 0.7573
                }
            ]
        }
        """
        dat_file = find_file(settings.HP_NN_FILE, self.work_dir)
        with open(dat_file, "r", encoding="utf-8") as fp:
            data = fp.read()

        RE_HP_NN_DATA = r"\s*V\s+{0}-{1}\s+{0}-{1}\s+{2}\s+{2}\s+{3}".format(
            ATOMIC_REGEX["atomicSpecies"],
            ATOMIC_REGEX["orbitalName"],
            GENERAL_REGEX["int_number"],
            GENERAL_REGEX["double_number"],
        )

        hp_data = re.findall(r"^{0}".format(RE_HP_NN_DATA), data, re.MULTILINE)

        values = []

        for row in hp_data:
            # split by white space and hyphen
            cols = re.sub(r"([\s\t\r\n-])+", " ", row.strip()).split(" ")
            values.append(
                {
                    "id": int(cols[5]),
                    "atomicSpecies": cols[1],
                    "orbitalName": cols[2],
                    "id2": int(cols[6]),
                    "atomicSpecies2": cols[3],
                    "orbitalName2": cols[4],
                    "value": float(cols[7]),
                }
            )

        return {
            "values": values,
        }
