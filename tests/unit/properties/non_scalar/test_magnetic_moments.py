from tests.unit import UnitTestBase
from tests.fixtures.data import MAGNETIC_MOMENTS_RAW_DATA
from express.properties.non_scalar.magnetic_moments import MagneticMoments

MAGNETIC_MOMENTS = {
    "units": "uB",
    "name": "magnetic_moments",
    "values": [{"id": 1, "value": [0, 0, 1.235]}, {"id": 2, "value": [0, 0, -1.235]}],
}


class MagneticMomentsTest(UnitTestBase):
    def setUp(self):
        super(MagneticMomentsTest, self).setUp()

    def tearDown(self):
        super(MagneticMomentsTest, self).setUp()

    def test_magnetic_moments(self):
        parser = self.get_mocked_parser("magnetic_moments", MAGNETIC_MOMENTS_RAW_DATA)
        property_ = MagneticMoments("magnetic_moments", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), MAGNETIC_MOMENTS)
