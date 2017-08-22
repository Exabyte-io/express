from tests.unit import UnitTestBase
from express.properties.scalar.total_energy import TotalEnergy

TOTAL_ENERGY = {
    "units": "eV",
    "name": "total_energy",
    "value": 1
}


class TotalEnergyTest(UnitTestBase):
    def setUp(self):
        super(TotalEnergyTest, self).setUp()

    def tearDown(self):
        super(TotalEnergyTest, self).setUp()

    def test_total_energy(self):
        property_ = TotalEnergy("total_energy", raw_data={"total_energy": 1})
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), TOTAL_ENERGY)
