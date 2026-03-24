from tests.unit import UnitTestBase
from express.properties.scalar.lumo_energy import LUMOEnergy

LUMO_ENERGY = {"units": "eV", "name": "lumo_energy", "value": 1}


class LUMOEnergyTest(UnitTestBase):
    def setUp(self):
        super(LUMOEnergyTest, self).setUp()

    def tearDown(self):
        super(LUMOEnergyTest, self).setUp()

    def test_lumo_energy(self):
        parser = self.get_mocked_parser("lumo_energy", 1)
        property_ = LUMOEnergy("lumo_energy", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), LUMO_ENERGY)
