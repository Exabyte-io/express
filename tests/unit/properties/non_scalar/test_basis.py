from tests.unit import UnitTestBase
from express.properties.non_scalar.basis import Basis
from tests.unit.properties.raw_data import BASIS_RAW_DATA

BASIS = {
    "name": "basis",
    "elements": [
        {
            "id": 1,
            "value": "Si"
        },
        {
            "id": 2,
            "value": "Si"
        }
    ],
    "coordinates": {
        "values": [
            {
                "id": 1,
                "value": [
                    0,
                    0,
                    0
                ]
            },
            {
                "id": 2,
                "value": [
                    0.25,
                    0.25,
                    0.25
                ]
            }
        ]
    },
    "units": "bohr"
}


class BasisTest(UnitTestBase):
    def setUp(self):
        super(BasisTest, self).setUp()

    def tearDown(self):
        super(BasisTest, self).setUp()

    def test_basis(self):
        property_ = Basis("basis", raw_data=BASIS_RAW_DATA)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), BASIS)
