import os
from express.parsers.settings import Constant
from express.parsers import BaseParser
from express.parsers.mixins.ionic import IonicDataMixin
from express.parsers.mixins.reciprocal import ReciprocalDataMixin
from express.parsers.mixins.electronic import ElectronicDataMixin
from express.parsers.apps.nwchem.formats.txt import NwchemTXTParser
from express.parsers.apps.nwchem import settings


class NwchemParser(BaseParser, IonicDataMixin, ElectronicDataMixin, ReciprocalDataMixin):
    """
    Nwchem parser class.
    """

    is_non_periodic = True

    def __init__(self, *args, **kwargs):
        super(NwchemParser, self).__init__(*args, **kwargs)
        self.work_dir = self.kwargs["work_dir"]
        self.stdout_file = self.kwargs["stdout_file"]
        self.txt_parser = NwchemTXTParser(self.work_dir)

    @staticmethod
    def _kcal_per_mol_to_ev(value):
        return value * Constant.kcal / Constant._Nav

    def total_energy(self):
        """
        Returns total energy.

        Reference:
            func: express.parsers.mixins.electronic.ElectronicDataMixin.total_energy
            NWChem energies are defaulted to hartrees and are converted to eV in this method
        """
        total_dft_energy = Constant.HARTREE * self.txt_parser.total_energy(self._get_file_content(self.stdout_file))
        return total_dft_energy

    def total_energy_contributions(self):
        """
        Extracts total energy contributions.

        Reference:
            func: express.parsers.mixins.electronic.ElectronicDataMixin.total_energy_contributions
            NWChem energies are defaulted to hartrees and are converted to eV in this method.
        """
        energy_contributions = self.txt_parser.total_energy_contributions(self._get_file_content(self.stdout_file))
        for key1, value1 in energy_contributions.items():
            for key2, value2 in value1.items():
                if type(value2) is float:
                    value1[key2] = value2 * Constant.HARTREE
        return energy_contributions

    def initial_basis(self):
        """
        Returns initial basis.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.initial_basis
        """
        return self.txt_parser.basis(self._get_file_content(self.stdout_file), 0)

    def final_basis(self):
        """
        Returns final basis.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.final_basis
        """
        return self.txt_parser.basis(self._get_file_content(self.stdout_file), -1)

    def eigenvalues_at_vectors(self):
        """
        Returns eigenvalues at molecular orbitals (vectors).

        Reference:
            func: express.parsers.mixins.electronic.ElectronicDataMixin.eigenvalues_at_vectors
            NWChem orbital energies are defaulted to hartrees and are converted to eV in this method.
        """
        orbitals = self.txt_parser.eigenvalues_at_vectors(self._get_file_content(self.stdout_file))
        return [dict(orbital, energy=Constant.HARTREE * orbital["energy"]) for orbital in orbitals]

    def homo_energy(self):
        """
        Returns HOMO energy, the highest energy among the occupied molecular orbitals.
        """
        energies = [orbital["energy"] for orbital in self.eigenvalues_at_vectors() if orbital["occupation"] > 0]
        return max(energies) if energies else None

    def lumo_energy(self):
        """
        Returns LUMO energy, the lowest energy among the unoccupied molecular orbitals.
        """
        energies = [orbital["energy"] for orbital in self.eigenvalues_at_vectors() if orbital["occupation"] == 0]
        return min(energies) if energies else None

    def zero_point_energy(self):
        """
        Returns zero point energy.

        Reference:
            NWChem zero-point correction is printed in kcal/mol and converted to eV in this method.
        """
        zero_point_energy = self.txt_parser.zero_point_energy(self._get_file_content(self.stdout_file))
        return None if zero_point_energy is None else self._kcal_per_mol_to_ev(zero_point_energy)

    def thermal_correction_to_energy(self):
        """
        Returns thermal correction to energy.

        Reference:
            NWChem thermochemistry correction is parsed directly in kcal/mol.
        """
        return self.txt_parser.thermal_correction_to_energy(self._get_file_content(self.stdout_file))

    def thermal_correction_to_enthalpy(self):
        """
        Returns thermal correction to enthalpy.
        """
        return self.txt_parser.thermal_correction_to_enthalpy(self._get_file_content(self.stdout_file))

    def _is_nwchem_output_file(self, path):
        """
        Checks whether the given file is nwchem output file.
        The file is considered nwchem output if it says 'Northwest Computational Chemistry Package' at the top.

        NOTE: DO NOT READ THE WHOLE FILE INTO MEMORY AS IT COULD BE BIG.

        Returns:
             bool
        """
        if os.path.exists(path):
            with open(path, "r") as f:
                for index, line in enumerate(f):
                    if index > 25:
                        break
                    if settings.NWCHEM_OUTPUT_FILE_REGEX in line:
                        return True
                return False

    def _find_nwchem_output_files(self):
        """
        Identifies the nwchem output files for parsing.

        Returns:
            str
        """
        nwchem_output_files = []
        for root, dirs, files in os.walk(self.work_dir, followlinks=True):
            for file in files:
                path = os.path.join(root, file)
                if self._is_nwchem_output_file(path):
                    nwchem_output_files.append(path)
        return nwchem_output_files
