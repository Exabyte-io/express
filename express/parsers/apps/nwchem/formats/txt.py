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

    def eigenvalues_at_vectors(self, text):
        """
        Extracts eigenvalues at molecular orbitals (vectors). Geometry optimizations print one
        orbital analysis section per step; the last one is read, for the final geometry.

        Units:
            energy: Hartree

        Args:
            text (str): text to extract data from.

        Returns:
            list[dict]
        """
        start_index = text.rfind(settings.ORBITAL_ANALYSIS_BLOCK_START_FLAG)
        if start_index == -1:
            return []
        return [
            {
                "vector": int(orbital.group("vector")),
                "occupation": _fortran_float(orbital.group("occupation")),
                "energy": _fortran_float(orbital.group("energy")),
            }
            for orbital in settings.VECTOR_REGEX.finditer(text[start_index:])
        ]

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
