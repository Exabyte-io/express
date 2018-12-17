import re
import numpy as np
from pymatgen.io.vasp import Outcar

from express.parsers.apps.vasp import settings
from express.parsers.formats.txt import BaseTXTParser


class VaspTXTParser(BaseTXTParser):
    """
    Vasp text parser class.
    """

    def __init__(self, work_dir):
        super(VaspTXTParser, self).__init__(work_dir)

    def ibz_kpoints(self, text, space):
        """
        Extracts kpoints coordinates in cartesian space.

        Args:
            text (str): text to extract data from.
            space (str): kpoints coordinate space, either crystal or cartesian.

        Returns:
            ndarray
        """
        text_range = {
            'cartesian': {
                'start': 'Following cartesian coordinates',
                'end': 'Dimension of arrays'
            },
            'crystal': {
                'start': 'Following reciprocal coordinates',
                'end': 'Following cartesian coordinates'
            }
        }
        start_index = text.find(text_range[space]['start'])
        end_index = text.find(text_range[space]['end'])
        ibz_kpts = re.findall(settings.REGEX["ibz_kpoints"]["regex"], text[start_index:end_index])
        ibz_kpts = [map(float, kp) for kp in ibz_kpts]
        return np.array(ibz_kpts)

    def total_energy(self, text):
        """
        Extracts total energy.

        Args:
            text (str): text to extract data from.

        Returns:
             float
        """
        return self._general_output_parser(text, **settings.REGEX["total_energy"])

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

        lattices = []
        match = re.findall(settings.REGEX["lattice_vectors"]["regex"], text)
        if match:
            for lattice in match:
                lattice = [float(_) for _ in lattice]
                lattices.append({
                    'vectors': {
                        'a': lattice[0:3],
                        'b': lattice[3:6],
                        'c': lattice[6:9],
                        'alat': 1.0  # abc vectors are expected in absolute units (eg. bohr)
                    }
                })
        return lattices

    def _basis_convergence(self, text, atom_names):
        """
        Extracts convergence bases computed in each BFGS step.

        Args:
            text (str): text to extract data from.
            atom_names (list): list of atom names.

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
        results = []
        matches = re.findall(settings.REGEX["ion_positions_block"]["regex"], text, re.DOTALL | re.MULTILINE)
        if matches:
            for match in matches:
                ions = re.findall(settings.REGEX["basis_vectors"]["regex"], match)
                results.append({
                    "units": "angstrom",
                    "elements": [{"id": idx, "value": atom_names[idx]} for idx in range(len(ions))],
                    "coordinates": [{"id": idx, "value": map(float, ion)} for idx, ion in enumerate(ions)]
                })
            return results

    def convergence_electronic(self, outcar, stdout, atom_names):
        """
        Extracts convergence electronic.
            1. Extract all energies (from dE column) along with the corresponding step [(1, 0.69948E+04), (2, -0.73973E+04)]
            2. Group the energies for each ionic step

        Sample input:
                   N       E                     dE             d eps       ncg     rms          rms(c)
            DAV:   1     0.699475439520E+04    0.69948E+04   -0.37054E+05   920   0.140E+03
            DAV:   2    -0.402547717878E+03   -0.73973E+04   -0.71440E+04  1084   0.442E+02
            DAV:   3    -0.105567783952E+04   -0.65313E+03   -0.64960E+03  1160   0.125E+02
            DAV:   4    -0.110887818556E+04   -0.53200E+02   -0.53162E+02  1560   0.284E+01
            DAV:   5    -0.111382548259E+04   -0.49473E+01   -0.49469E+01  1240   0.562E+00    0.137E+02
                1 T=  2001. E= -.89713765E+03 F= -.92170983E+03 E0= -.92172095E+03  EK= 0.24572E+02

                   N       E                     dE             d eps       ncg     rms          rms(c)
            DAV:   1    -0.916206954626E+03    0.55030E+01   -0.19221E+03   920   0.750E+01    0.931E+00
            DAV:   2    -0.920149095159E+03   -0.39421E+01   -0.47144E+01  1072   0.109E+01    0.625E+00
            DAV:   3    -0.919835295300E+03    0.31380E+00   -0.27646E+00  1288   0.256E+00    0.367E+00
            DAV:   4    -0.919705445969E+03    0.12985E+00   -0.93950E-01  1128   0.186E+00    0.145E+00
                2 T=  1843. E= -.89706481E+03 F= -.91969309E+03 E0= -.91970717E+03  EK= 0.22628E+02

        Args:
            outcar (str): OUTCAR content.
            stdout (str): stdout content.
            atom_names (list): list of atoms.

        Returns:
             list[list]
        """
        data = []
        matches = self._general_output_parser(stdout, **settings.REGEX["convergence_electronic"])
        first_step_indices = [ind for ind, elm in enumerate(matches) if int(elm[0]) == 1]
        for ind, first_step_index in enumerate(first_step_indices):
            if ind + 1 == len(first_step_indices):
                energies = matches[first_step_index:]
            else:
                energies = matches[first_step_index:first_step_indices[ind + 1]]
            data.append([energy[1] for energy in energies])  # strip out the step numbers
        return data

    def convergence_ionic(self, outcar, stdout, atom_names):
        """
        Extracts convergence ionic.

        Args:
            outcar (str): OUTCAR content.
            stdout (str): stdout content.
            atom_names (list): list of atoms.

        Returns:
             list[dict]
        """
        data = []
        convergence_electronic_data = self.convergence_electronic(outcar, stdout, atom_names)
        for ind, energies in enumerate(convergence_electronic_data):
            data.append({
                "energy": sum([sum(e) for e in convergence_electronic_data[0:ind + 1]]),
                "electronic": {
                    "units": "eV",
                    "data": energies
                },
            })

        if not data: return []

        lattice_convergence = self._lattice_convergence(outcar)
        basis_convergence = self._basis_convergence(outcar, atom_names)
        data = data[0:len(lattice_convergence)]  # strip out the last non-complete step
        if not data: return []
        for idx, structure in enumerate(zip(lattice_convergence, basis_convergence)):
            data[idx].update({
                'structure': {
                    'lattice': structure[0],
                    'basis': structure[1]
                }
            })

        return data

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

        Args:
            text (str): text to extract data from.

        Returns:
            float
        """
        total_force = self._general_output_parser(text, **settings.REGEX['total_force'])
        return np.sqrt(np.sum(np.square(total_force)))

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
            if value:
                energy_contributions.update({contribution: {
                    'name': contribution,
                    'value': np.sqrt(np.sum(np.square(value)))
                }})
        return energy_contributions

    def zero_point_energy(self, text):
        """
        Extracts zero point energy.

        Returns:
             float
        """
        data = self._general_output_parser(text, **settings.REGEX['zero_point_energy'])
        return sum(data) / 2 / 1000

    def magnetic_moments(self, outcar):
        """
        Extracts magnetic moments.

        Returns:
             list
        """
        mag = Outcar(outcar).magnetization
        return [[0, 0, ion['tot']] if isinstance(ion['tot'], float) else ion['tot'].moment.tolist() for ion in mag]
