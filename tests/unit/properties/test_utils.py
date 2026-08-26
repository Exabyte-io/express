import unittest

from express.parsers.mixins.ionic import IonicDataMixin
from express.properties.material import Material
from express.properties.utils import box_molecule


def basis(coordinates):
    return {
        "units": "angstrom",
        "elements": [{"id": idx, "value": "H"} for idx, _ in enumerate(coordinates)],
        "coordinates": [{"id": idx, "value": value} for idx, value in enumerate(coordinates)],
    }


COMPACT = basis([[0.0, 0.0, 0.2], [0.0, 0.0, -0.2]])
EXPANDED = basis([[0.0, 0.0, 2.5], [0.0, 0.0, -2.5]])


class RelaxationThatExpandsParser(IonicDataMixin):
    is_non_periodic = True

    def initial_basis(self):
        return COMPACT

    def final_basis(self):
        return EXPANDED


class BoxMoleculeTest(unittest.TestCase):
    """
    A relaxation that expands, which no committed fixture covers and which is the direction that
    corrupts data: size the cell from the compact structure, centre the expanded one in it, and atoms
    land outside the box, where they read as extra fragments and wreck the InChI.
    """

    def edge(self, selected_basis, parsed_bases):
        return box_molecule(selected_basis, parsed_bases)[0]["vectors"]["a"][0]

    def test_cell_is_sized_to_the_largest_structure(self):
        self.assertEqual(self.edge(COMPACT, [COMPACT, EXPANDED]), self.edge(EXPANDED, [EXPANDED]))
        self.assertGreater(self.edge(EXPANDED, [EXPANDED]), self.edge(COMPACT, [COMPACT]))

    def test_every_structure_is_centered_inside_the_shared_cell(self):
        for selected_basis in (COMPACT, EXPANDED):
            lattice, centered = box_molecule(selected_basis, [COMPACT, EXPANDED])
            edge = lattice["vectors"]["a"][0]
            for coordinate in centered["coordinates"]:
                self.assertTrue(all(0.0 <= value <= edge for value in coordinate["value"]))

    def test_material_hands_over_every_parsed_basis(self):
        parser = RelaxationThatExpandsParser()
        lattices = [
            Material("material", parser, **{kwarg: True}).lattice
            for kwarg in ("is_initial_structure", "is_final_structure")
        ]
        self.assertEqual(lattices[0], lattices[1])
        self.assertAlmostEqual(lattices[0]["a"], self.edge(EXPANDED, [EXPANDED]), places=6)
