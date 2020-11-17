import os
import io
import re
import numpy as np

from express.parsers.utils import find_file
from express.parsers.settings import Constant
from express.parsers.apps.nwchem import settings
from express.parsers.formats.txt import BaseTXTParser


class NwchemTXTParser(BaseTXTParser):
    """
    Nwchem text parser class.
    """

    def __init__(self, work_dir):
        super(NwchemTXTParser, self).__init__(work_dir)

    def total_energy(self, text):
        """
        Extracts total energy.

        Args:
            text (str): text to extract data from.

        Returns:
             float
        """
        print(self._general_output_parser(text, **settings.regex["total_energy"]))
        return self._general_output_parser(text, **settings.regex["total_energy"])

    # NEED TO CHECK MATH/UNITS ON TOTAL ENERGY CONTRIBUTION
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
                    'value': np.sum(value)
                }})
        return energy_contributions
