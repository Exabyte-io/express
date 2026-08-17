from mat3ra.made.tools.convert.utils import calculate_padded_cell_simple_cubic
from mat3ra.made.utils import get_center_of_coordinates

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

    def _geometry_block(self, text, last):
        """
        Extracts one "Output coordinates" block as coordinates in angstrom.

        A geometry optimization prints one block per step; a single-point run prints exactly one, so
        the first and the last block coincide and the initial and final structures are equal. The
        block is printed in whichever units the input declared, and the header carries the factor
        converting them to a.u., so both `units angstrom` and `units au` runs are read correctly.

        Args:
            text (str): text to extract data from.
            last (bool): whether to read the last block instead of the first.

        Returns:
            tuple[list[str], list[list[float]]]: elements and coordinates in angstrom.
        """
        blocks = list(settings.GEOMETRY_BLOCK_REGEX.finditer(text))
        if not blocks:
            return [], []

        block = blocks[-1] if last else blocks[0]
        # An `angstroms` block is taken verbatim; rescaling it through two Bohr radii that disagree
        # in the last digits would perturb coordinates the file already gives exactly.
        is_angstrom = block.group("units").startswith("angstrom")
        to_angstrom = 1.0 if is_angstrom else float(block.group("scale")) * Constant.BOHR

        rows = list(settings.GEOMETRY_ROW_REGEX.finditer(block.group("rows")))
        return (
            [row.group("element") for row in rows],
            [[float(row.group(axis)) * to_angstrom for axis in ("x", "y", "z")] for row in rows],
        )

    def _basis(self, text, last):
        """
        Extracts a basis, centered inside the cell that `_lattice_vectors` derives for the same
        block. NWChem's coordinates straddle the origin and would otherwise sit outside the box.

        Args:
            text (str): text to extract data from.
            last (bool): whether to read the last block instead of the first.

        Returns:
            dict

        Example:
            {
                'units': 'angstrom',
                'elements': [{'id': 0, 'value': 'O'}, {'id': 1, 'value': 'H'}],
                'coordinates': [{'id': 0, 'value': [2.86, 2.86, 3.60]}, {'id': 1, 'value': [1.43, 2.86, 2.49]}]
            }
        """
        elements, coordinates = self._geometry_block(text, last)
        if not elements:
            return None

        # Take the edge from _lattice_vectors rather than deriving a second cell here, so the basis
        # is centered in the very box that ships with it.
        center = get_center_of_coordinates(coordinates)
        box_center = self._lattice_vectors(text)["vectors"]["a"][0] / 2
        return {
            "units": "angstrom",
            "elements": [{"id": index, "value": value} for index, value in enumerate(elements)],
            "coordinates": [
                {"id": index, "value": [x - center[axis] + box_center for axis, x in enumerate(coordinate)]}
                for index, coordinate in enumerate(coordinates)
            ],
        }

    def _lattice_vectors(self, text):
        """
        Derives a cell for a molecule, which NWChem does not print: made's simple-cubic padding
        convention, the same one that gives every non-periodic material on the platform its box.

        One cell for both structures, so they are comparable: an optimization moves atoms inside a
        fixed box rather than resizing it. Sized to whichever of the two geometries needs more room,
        because a relaxation that expands the molecule would otherwise leave atoms outside a box
        derived from the initial one -- which reads as extra fragments and corrupts the InChI.

        Args:
            text (str): text to extract data from.

        Returns:
            dict

        Example:
            {'vectors': {'a': [5.72, 0.0, 0.0], 'b': [0.0, 5.72, 0.0], 'c': [0.0, 0.0, 5.72], 'alat': 1}}
        """
        edges = [
            calculate_padded_cell_simple_cubic(coordinates)[0][0]
            for coordinates in (self._geometry_block(text, last)[1] for last in (False, True))
            if coordinates
        ]
        if not edges:
            return None

        edge = max(edges)
        return {"vectors": {"a": [edge, 0.0, 0.0], "b": [0.0, edge, 0.0], "c": [0.0, 0.0, edge], "alat": 1}}

    def initial_basis(self, text):
        return self._basis(text, last=False)

    def final_basis(self, text):
        return self._basis(text, last=True)

    def initial_lattice_vectors(self, text):
        return self._lattice_vectors(text)

    def final_lattice_vectors(self, text):
        return self._lattice_vectors(text)

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
