from tests.unit import UnitTestBase
from tests.data.raw_data import SYMMETRY_RAW_DATA
from express.properties.non_scalar.symmetry import Symmetry

SYMMETRY = {
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
        property_ = Symmetry("symmetry", raw_data=SYMMETRY_RAW_DATA)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), SYMMETRY)
