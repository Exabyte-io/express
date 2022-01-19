from tests.unit import UnitTestBase
from tests.fixtures.data import POINT_GROUP_SYMBOL
from express.properties.structural.point_group_symmetry import PointGroupSymmetry

POINT_GROUP_SYMMETRY = {
    "name": "symmetry_symbol_point_group",
    "value": "Cv2",
    "tolerance": {
        "value": 0.3,
        "units": "angstrom"
    }
}


class PointGroupSymmetryTest(UnitTestBase):
    def setUp(self):
        super(PointGroupSymmetryTest, self).setUp()

    def tearDown(self):
        super(PointGroupSymmetryTest, self).setUp()

    def test_point_group_symmetry(self):
        parser = self.get_mocked_parser("point_group_symbol", POINT_GROUP_SYMBOL)
        property_ = PointGroupSymmetry("symmetry_symbol_point_group", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), POINT_GROUP_SYMMETRY)
