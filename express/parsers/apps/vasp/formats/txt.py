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
        energies = self._general_output_parser(stdout, **settings.REGEX["convergence_ionic_energies"])
        indices = [i for i, e in enumerate(energies) if e[0] == 1.0]
        ionic_energies = [[e[1] for e in energies[i:indices[ind + 1]]] if (ind + 1) < len(indices) else energies[i:] for ind, i in enumerate(indices)]
        for energies in ionic_energies:
            data.append({
                "energy": energies[-1],
                "electronic": {
                    "units": "eV",
                    "data": energies
                },
            })

        if not data: return []

        lattice_convergence = self._lattice_convergence(outcar)
        basis_convergence = self._basis_convergence(outcar, atom_names)
        for idx, structure in enumerate(zip(lattice_convergence, basis_convergence)):
            data[idx].update({
                'structure': {
                    'lattice': structure[0],
                    'basis': structure[1]
                }
            })

        return data

    def convergence_electronic(self, outcar, stdout, atom_names):
        """
        Extracts convergence electronic.

        Args:
            outcar (str): OUTCAR content.
            stdout (str): stdout content.
            atom_names (list): list of atoms.

        Returns:
             list[float]
        """
        data = self._general_output_parser(stdout, **settings.REGEX["convergence_electronic"])
        # The next 3 lines are necessary to have realtime data
        ionic_data = [_["electronic"]["data"] for _ in self.convergence_ionic(outcar, stdout, atom_names)]
        last_step_data = data[sum([len(_) for _ in ionic_data]): len(data)]
        if last_step_data: ionic_data.append(last_step_data)
        return ionic_data

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
