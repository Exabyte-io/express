from tests.unit import UnitTestBase
from express.properties.non_scalar.basis import Basis

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
    "units": "angstrom"
}


class BasisTest(UnitTestBase):
    def setUp(self):
        super(BasisTest, self).setUp()

    def tearDown(self):
        super(BasisTest, self).setUp()

    def test_basis(self):
        raw_data = {
            "basis": {
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
            }
        }
        property_ = Basis("basis", raw_data=raw_data)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), BASIS)
