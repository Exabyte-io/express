from tests.unit import UnitTestBase
from tests.fixtures.data import SPACE_GROUP_SYMBOL
from express.properties.scalar.symmetry_symbol_space_group import SymmetrySymbolSpaceGroup

SPACE_GROUP_SYMMETRY = {
    "name": "symmetry_symbol_space_group",
    "value": "Fd-3m",
    "tolerance": {
        "value": 0.3,
        "units": "angstrom"
    }
}


class SymmetrySymbolSpaceGroupTest(UnitTestBase):
    def setUp(self):
        super(SymmetrySymbolSpaceGroupTest, self).setUp()

    def tearDown(self):
        super(SymmetrySymbolSpaceGroupTest, self).setUp()

    def test_symmetry_symbol_space_group(self):
        parser = self.get_mocked_parser("symmetry_symbol_space_group", SPACE_GROUP_SYMBOL)
        property_ = SymmetrySymbolSpaceGroup("symmetry_symbol_space_group", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), SPACE_GROUP_SYMMETRY)
