from tests.unit import UnitTestBase
from express.properties.non_scalar.lattice import Lattice

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
        raw_data = {
            "lattice_vectors": {
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

                "units": "angstrom"
            }

        }
        property_ = Lattice("lattice", raw_data=raw_data)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), LATTICE)
