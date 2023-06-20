from tests.unit import UnitTestBase
from express.properties.scalar.zero_point_energy import ZeroPointEnergy

ZERO_POINT_ENERGY = {"units": "eV", "name": "zero_point_energy", "value": 1}


class TotalZeroPointTest(UnitTestBase):
    def setUp(self):
        super(TotalZeroPointTest, self).setUp()

    def tearDown(self):
        super(TotalZeroPointTest, self).setUp()

    def test_zero_point_energy(self):
        parser = self.get_mocked_parser("zero_point_energy", 1)
        property_ = ZeroPointEnergy("zero_point_energy", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), ZERO_POINT_ENERGY)
