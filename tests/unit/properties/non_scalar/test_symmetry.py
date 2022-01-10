from mock import MagicMock

from tests.unit import UnitTestBase
from tests.fixtures.data import SPACE_GROUP_SYMBOL
from tests.fixtures.data import POINT_GROUP_SYMBOL
from express.properties.non_scalar.symmetry import Symmetry

SYMMETRY = {
    "pointGroupSymbol": "Cv2",
    "spaceGroupSymbol": "Fd-3m",
    "tolerance": {
        "value": 0.3,
        "units": "angstrom"
    },
    "name": "symmetry"
}


class SymmetryTest(UnitTestBase):
    def setUp(self):
        super(SymmetryTest, self).setUp()

    def tearDown(self):
        super(SymmetryTest, self).setUp()

    def test_symmetry(self):
        parser = self.get_mocked_parser("space_group_symbol", SPACE_GROUP_SYMBOL)
        parser.attach_mock(MagicMock(return_value=POINT_GROUP_SYMBOL), "point_group_symbol")
        property_ = Symmetry("symmetry", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), SYMMETRY)
