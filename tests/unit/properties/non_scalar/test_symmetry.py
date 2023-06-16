from tests.unit import UnitTestBase
from tests.fixtures.data import SPACE_GROUP_SYMBOL
from express.properties.non_scalar.symmetry import Symmetry

SYMMETRY = {"spaceGroupSymbol": "Fd-3m", "tolerance": {"value": 0.3, "units": "angstrom"}, "name": "symmetry"}


class SymmetryTest(UnitTestBase):
    def setUp(self):
        super(SymmetryTest, self).setUp()

    def tearDown(self):
        super(SymmetryTest, self).setUp()

    def test_symmetry(self):
        parser = self.get_mocked_parser("space_group_symbol", SPACE_GROUP_SYMBOL)
        property_ = Symmetry("symmetry", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), SYMMETRY)
