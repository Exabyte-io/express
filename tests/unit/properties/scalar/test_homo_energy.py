from tests.unit import UnitTestBase
from express.properties.scalar.homo_energy import HOMOEnergy

HOMO_ENERGY = {"units": "eV", "name": "homo_energy", "value": 1}


class HOMOEnergyTest(UnitTestBase):
    def setUp(self):
        super(HOMOEnergyTest, self).setUp()

    def tearDown(self):
        super(HOMOEnergyTest, self).setUp()

    def test_homo_energy(self):
        parser = self.get_mocked_parser("homo_energy", 1)
        property_ = HOMOEnergy("homo_energy", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), HOMO_ENERGY)
