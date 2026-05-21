import os

from tests.unit import UnitTestBase
from tests.fixtures.structural.references import LI_CIF_BASIS
from express.parsers.structure import StructureParser

LI_CIF_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "fixtures", "structural", "test-004", "Li.cif")

DISORDERED_CIF_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "fixtures", "structural", "test-004", "SrLaCoO4.cif"
)


def _read_file(path):
    with open(path) as f:
        return f.read()


class LiCifStructureParserTest(UnitTestBase):
    """
    Tests that StructureParser correctly handles CIF files containing oxidation
    state labels (e.g. Li0+), stripping them to plain element symbols (Li).
    """

    def setUp(self):
        super().setUp()
        self.parser = StructureParser(
            structure_string=_read_file(LI_CIF_PATH),
            structure_format="cif",
        )

    def tearDown(self):
        super().tearDown()

    def test_parser_strips_oxidation_state_suffix(self):
        """
        Verifies the full basis: element symbols (Li0+ -> Li) and
        fractional coordinates are both parsed correctly.
        """
        self.assertDeepAlmostEqual(self.parser.basis(), LI_CIF_BASIS, places=5)


class DisorderedStructureParserTest(UnitTestBase):
    """
    Tests that StructureParser raises a ValueError with an informative message
    when basis() is called on a structure with disordered (mixed-occupancy) sites.

    The SrLaCoO4 CIF has Sr2+ and La3+ sharing the same Wyckoff 4e site
    with occupancy 0.5 each — a canonical disordered case.
    """

    def setUp(self):
        super().setUp()
        # Parsing itself succeeds — pymatgen can load disordered structures.
        # The error is raised lazily when basis() is called.
        self.parser = StructureParser(
            structure_string=_read_file(DISORDERED_CIF_PATH),
            structure_format="cif",
        )

    def tearDown(self):
        super().tearDown()

    def test_basis_raises_for_disordered_site(self):
        """
        basis() must raise ValueError for mixed-occupancy sites.
        The error message should identify the site coordinates and occupancy.
        """
        with self.assertRaises(ValueError) as ctx:
            self.parser.basis()
        error = str(ctx.exception)
        self.assertIn("is not supported", error)
        self.assertIn("occupancy", error)
        self.assertIn("0.361", error)
