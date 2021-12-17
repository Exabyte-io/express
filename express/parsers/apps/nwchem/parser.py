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

    def __init__(self, *args, **kwargs):
        super(NwchemParser, self).__init__(*args, **kwargs)
        self.work_dir = self.kwargs["work_dir"]
        self.stdout_file = self.kwargs["stdout_file"]
        self.txt_parser = NwchemTXTParser(self.work_dir)

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
                if type(value2) == float:
                    value1[key2] = value2 * Constant.HARTREE
        return energy_contributions

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
