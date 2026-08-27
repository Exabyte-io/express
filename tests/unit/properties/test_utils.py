import unittest

from express.parsers.mixins.ionic import IonicDataMixin
from express.properties.material import Material
from express.properties.utils import box_molecule, to_array_with_ids


def basis(*heights):
    return {
        "units": "angstrom",
        "elements": to_array_with_ids(["H"] * len(heights)),
        "coordinates": to_array_with_ids([[0.0, 0.0, height] for height in heights]),
    }


COMPACT, EXPANDED = basis(0.2, -0.2), basis(2.5, -2.5)
EXPANDED_EDGE = 15.0
STRUCTURE_KWARGS = ("is_initial_structure", "is_final_structure")


class ExpandingRelaxationParser(IonicDataMixin):
    is_non_periodic = True

    def initial_basis(self):
        return COMPACT

    def final_basis(self):
        return EXPANDED


class BoxMoleculeTest(unittest.TestCase):
    def test_shared_cell_holds_a_relaxation_that_expands(self):
        # No committed fixture relaxes outward, and that is the direction that leaves atoms outside
        # the box, where they read as extra fragments and corrupt the InChI.
        for selected_basis in (COMPACT, EXPANDED):
            lattice, centered = box_molecule(selected_basis, [COMPACT, EXPANDED])
            self.assertEqual(lattice["vectors"]["a"][0], EXPANDED_EDGE)
            for coordinate in centered["coordinates"]:
                self.assertTrue(all(0.0 <= x <= EXPANDED_EDGE for x in coordinate["value"]))

    def test_material_hands_over_every_parsed_basis(self):
        parser = ExpandingRelaxationParser()
        lattices = [Material("material", parser, **{kwarg: True}).lattice for kwarg in STRUCTURE_KWARGS]
        self.assertEqual(lattices[0], lattices[1])
        self.assertAlmostEqual(lattices[0]["a"], EXPANDED_EDGE, places=6)
