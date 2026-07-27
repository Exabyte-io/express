from express.parsers.settings import Constant  # noqa: F401
from express.parsers.apps.nwchem import settings
from express.parsers.formats.txt import BaseTXTParser


def _fortran_float(value):
    """
    Converts a Fortran-formatted float string (e.g. "-1.234D+01", double-precision
    "D" exponent notation) to a Python float.

    Args:
        value (str): Fortran-formatted number, e.g. "-1.234D+01".

    Returns:
        float
    """
    return float(value.replace("D", "E").replace("d", "e"))


class NwchemTXTParser(BaseTXTParser):
    """
    Nwchem text parser class.
    """

    def __init__(self, work_dir):
        super(NwchemTXTParser, self).__init__(work_dir)

    def _converged_orbital_block(self, text):
        """
        Returns the text of the final molecular orbital analysis section, or an empty
        string if it is not present.

        Args:
            text (str): text to extract data from.

        Returns:
            str
        """
        start_index = text.rfind(settings.FRONTIER_ORBITAL_BLOCK_START_FLAG)
        return text[start_index:] if start_index != -1 else ""

    def _converged_homo_energy(self, text):
        """
        Extracts the HOMO energy (Hartree): the highest energy among occupied orbitals.

        Args:
            text (str): text to extract data from.

        Returns:
            float | None
        """
        occupied_energies = [
            _fortran_float(orbital.group("energy"))
            for orbital in settings.VECTOR_REGEX.finditer(self._converged_orbital_block(text))
            if _fortran_float(orbital.group("occupation")) > 0
        ]
        return max(occupied_energies) if occupied_energies else None

    def _converged_lumo_energy(self, text):
        """
        Extracts the LUMO energy (Hartree): the lowest energy among unoccupied orbitals.

        Args:
            text (str): text to extract data from.

        Returns:
            float | None
        """
        virtual_energies = [
            _fortran_float(orbital.group("energy"))
            for orbital in settings.VECTOR_REGEX.finditer(self._converged_orbital_block(text))
            if _fortran_float(orbital.group("occupation")) == 0
        ]
        return min(virtual_energies) if virtual_energies else None

    def total_energy(self, text):
        """
        Extracts total energy.

        Args:
            text (str): text to extract data from.

        Returns:
             float
        """
        return self._general_output_parser(text, **settings.REGEX["total_energy"])

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
                energy_contributions.update({contribution: {"name": contribution, "value": value}})
        return energy_contributions

    def homo_energy(self, text):
        """
        Extracts the converged HOMO energy.

        Args:
            text (str): text to extract data from.

        Returns:
            float | None
        """
        return self._converged_homo_energy(text)

    def lumo_energy(self, text):
        """
        Extracts the converged LUMO energy.

        Args:
            text (str): text to extract data from.

        Returns:
            float | None
        """
        return self._converged_lumo_energy(text)

    def zero_point_energy(self, text):
        """
        Extracts zero point energy.

        Args:
            text (str): text to extract data from.

        Returns:
            float | None
        """
        return self._general_output_parser(text, **settings.REGEX["zero_point_energy"])

    def thermal_correction_to_energy(self, text):
        """
        Extracts thermal correction to energy.

        Args:
            text (str): text to extract data from.

        Returns:
            float | None
        """
        return self._general_output_parser(text, **settings.REGEX["thermal_correction_to_energy"])

    def thermal_correction_to_enthalpy(self, text):
        """
        Extracts thermal correction to enthalpy.

        Args:
            text (str): text to extract data from.

        Returns:
            float | None
        """
        return self._general_output_parser(text, **settings.REGEX["thermal_correction_to_enthalpy"])
