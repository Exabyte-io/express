from tests.unit import UnitTestBase
from express.properties.non_scalar.stress_tensor import StressTensor

STRESS_TENSOR = {
    "name": "stress_tensor",
    "value": [
        [
            3,
            0,
            0
        ],
        [
            0,
            3,
            0
        ],
        [
            0,
            0,
            3
        ]
    ],
    "units": "kbar"
}


class StressTensorTest(UnitTestBase):
    def setUp(self):
        super(StressTensorTest, self).setUp()

    def tearDown(self):
        super(StressTensorTest, self).setUp()

    def test_stress_tensor(self):
        raw_data = {
            "stress_tensor": [
                [
                    3,
                    0,
                    0
                ],
                [
                    0,
                    3,
                    0
                ],
                [
                    0,
                    0,
                    3
                ]
            ]
        }
        property_ = StressTensor("stress_tensor", raw_data=raw_data)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), STRESS_TENSOR)
