from tests.unit import UnitTestBase
from tests.data.raw_data import STRESS_TENSOR_RAW_DATA
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
        property_ = StressTensor("stress_tensor", raw_data=STRESS_TENSOR_RAW_DATA)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), STRESS_TENSOR)
