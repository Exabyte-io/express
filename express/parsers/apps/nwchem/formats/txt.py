from express.parsers.settings import Constant
from express.parsers.apps.nwchem import settings
from express.parsers.formats.txt import BaseTXTParser
from express.parsers.utils import _fortran_float


class NwchemTXTParser(BaseTXTParser):
    """
    Nwchem text parser class.
    """

    def __init__(self, work_dir):
        super(NwchemTXTParser, self).__init__(work_dir)

    def geometry_blocks(self, text):
        """
        Extracts every "Output coordinates" block, or nothing at all if they disagree on which
        atoms are present. A log truncated mid-table parses as a shorter molecule, and the callers
        below cannot tell that from a real one -- rupy would publish the fragment as
        `final_structure`, formula and InChI included.

        A block is printed in whichever units the input declared, and its header carries the factor
        converting them to a.u., so both `units angstrom` and `units au` runs are read correctly.

        Args:
            text (str): text to extract data from.

        Returns:
            list[tuple[list[str], list[list[float]]]]: elements and coordinates in angstrom.
        """
        blocks = []
        for block in settings.GEOMETRY_BLOCK_REGEX.finditer(text):
            to_angstrom = float(block.group("scale")) * Constant.BOHR
            rows = list(settings.GEOMETRY_ROW_REGEX.finditer(block.group("rows")))
            blocks.append(
                (
                    [row.group("element") for row in rows],
                    [[float(row.group(axis)) * to_angstrom for axis in ("x", "y", "z")] for row in rows],
                )
            )
        if len({tuple(elements) for elements, _ in blocks}) > 1:
            return []
        return blocks

    def basis(self, text, index):
        """
        Extracts the geometry block at the given index. An optimization prints one block per step;
        a single-point run prints exactly one, so index 0 and index -1 then coincide.

        Args:
            text (str): text to extract data from.
            index (int): position of the block among those printed.

        Returns:
            dict | None

        Example:
            {
                'units': 'angstrom',
                'elements': [{'id': 0, 'value': 'O'}, {'id': 1, 'value': 'H'}],
                'coordinates': [{'id': 0, 'value': [0.0, 0.0, 0.11]}, {'id': 1, 'value': [0.0, 0.75, -0.46]}]
            }
        """
        blocks = self.geometry_blocks(text)
        if not blocks:
            return None

        elements, coordinates = blocks[index]
        return {
            "units": "angstrom",
            "elements": [{"id": idx, "value": value} for idx, value in enumerate(elements)],
            "coordinates": [{"id": idx, "value": coordinate} for idx, coordinate in enumerate(coordinates)],
        }

    def eigenvalues_at_vectors(self, text):
        """
        Extracts eigenvalues at molecular orbitals (vectors). Geometry optimizations print one
        orbital analysis section per step; the last one is read, for the final geometry. A
        spin-polarized run prints an alpha and a beta section per step, both of which are read.

        Units:
            energy: Hartree

        Args:
            text (str): text to extract data from.

        Returns:
            list[dict]
        """
        blocks = list(settings.ORBITAL_ANALYSIS_BLOCK_REGEX.finditer(text))
        ends = [block.start() for block in blocks[1:]] + [len(text)]
        last_block_per_spin = {block.group("spin"): text[block.end() : end] for block, end in zip(blocks, ends)}
        return [
            {
                "vector": int(orbital.group("vector")),
                "occupation": _fortran_float(orbital.group("occupation")),
                "energy": _fortran_float(orbital.group("energy")),
            }
            for block in last_block_per_spin.values()
            for orbital in settings.VECTOR_REGEX.finditer(block)
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
