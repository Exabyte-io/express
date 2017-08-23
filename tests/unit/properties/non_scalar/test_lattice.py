from tests.unit import UnitTestBase
from express.properties.non_scalar.lattice import Lattice
from tests.unit.properties.raw_data import LATTICE_RAW_DATA

LATTICE = {
    "vectors": {
        "a": [
            5.000000000,
            0.000121312,
            0.000131415
        ],
        "b": [
            0.000121312,
            5.000000000,
            0.000121314
        ],
        "c": [
            0.000121313,
            0.000121312,
            5.000000000
        ],
        "alat": 1.0,
    },
    "units": "angstrom",
    "name": "lattice"
}


class LatticeTest(UnitTestBase):
    def setUp(self):
        super(LatticeTest, self).setUp()

    def tearDown(self):
        super(LatticeTest, self).setUp()

    def test_lattice(self):
        property_ = Lattice("lattice", raw_data=LATTICE_RAW_DATA)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), LATTICE)
