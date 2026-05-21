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

    def test_basis_parsing_of_oxidation_state_suffix(self):
        """
        Verifies the full basis: element symbols (Li0+ -> Li) and
        fractional coordinates are both parsed correctly.
        """
        self.assertDeepAlmostEqual(self.parser.basis(), LI_CIF_BASIS, places=5)
