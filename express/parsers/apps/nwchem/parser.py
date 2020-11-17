import os
import numpy as np

from express.parsers import BaseParser
from express.parsers.apps.nwchem import settings
from express.parsers.mixins.ionic import IonicDataMixin
from express.parsers.apps.nwchem.formats.txt import NwchemTXTParser
from express.parsers.mixins.reciprocal import ReciprocalDataMixin
from express.parsers.mixins.electronic import ElectronicDataMixin
from express.parsers.utils import find_file, find_fines_by_name_substring


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
        """
        print(self._get_file_content(self.stdout_file))
        total_dft_energy = self.txt_parser.total_energy(self._get_file_content(self.stdout_file))
        #total_dft_energy = 27.2114 * hartrees
        return total_dft_energy 

    def total_energy_contributions(self):
        """
        Extracts total energy contributions.

        Reference:
            func: express.parsers.mixins.electronic.ElectronicDataMixin.total_energy_contributions
        """
        return self.txt_parser.total_energy_contributions(self._get_file_content(self.stdout_file))

    def _find_nwchem_output_files(self):
        nwchem_output_files = []
        for root, dirs, files in os.walk(self.work_dir, followlinks=True):
            for file in files:
                path = os.path.join(root, file)
                if self._is_nwchem_output_file(path):
                    nwchem_output_files.append(path)
        return nwchem_output_files
