from tests.unit import UnitTestBase
from tests.fixtures.data import POINT_GROUP_SYMBOL
from express.properties.scalar.symmetry_symbol_point_group import SymmetrySymbolPointGroup

POINT_GROUP_SYMMETRY = {
    "name": "symmetry_symbol_point_group",
    "value": "Cv2",
    "tolerance": {
        "value": 0.3,
        "units": "angstrom"
    }
}


class SymmetrySymbolPointGroupTest(UnitTestBase):
    def setUp(self):
        super(SymmetrySymbolPointGroupTest, self).setUp()

    def tearDown(self):
        super(SymmetrySymbolPointGroupTest, self).setUp()

    def test_symmetry_symbol_point_group(self):
        parser = self.get_mocked_parser("symmetry_symbol_point_group", POINT_GROUP_SYMBOL)
        property_ = SymmetrySymbolPointGroup("symmetry_symbol_point_group", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), POINT_GROUP_SYMMETRY)
