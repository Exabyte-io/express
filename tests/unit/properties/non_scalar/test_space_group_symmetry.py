from tests.unit import UnitTestBase
from tests.fixtures.data import SPACE_GROUP_SYMBOL
from express.properties.structural.space_group_symmetry import SpaceGroupSymmetry

SPACE_GROUP_SYMMETRY = {
    "value": "Fd-3m",
    "tolerance": {
        "value": 0.3,
        "units": "angstrom",
    },
    "name": "symmetry_symbol_space_group"
}


class SpaceGroupSymmetryTest(UnitTestBase):
    def setUp(self):
        super(SpaceGroupSymmetryTest, self).setUp()

    def tearDown(self):
        super(SpaceGroupSymmetryTest, self).setUp()

    def test_space_group_symmetry(self):
        parser = self.get_mocked_parser("space_group_symbol", SPACE_GROUP_SYMBOL)
        property_ = SpaceGroupSymmetry("symmetry_symbol_space_group", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), SPACE_GROUP_SYMMETRY)
