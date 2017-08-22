from tests.unit import UnitTestBase
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

    def test_atomic_forces(self):
        raw_data = {
            "space_group_symbol": {
                "value": "Fd-3m",
                "tolerance": 0.3
            }
        }
        property_ = Symmetry("symmetry", raw_data=raw_data)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), SYMMETRY)
