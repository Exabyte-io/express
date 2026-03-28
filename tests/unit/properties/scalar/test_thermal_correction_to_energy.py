from tests.unit import UnitTestBase
from express.properties.scalar.thermal_correction_to_energy import ThermalCorrectionToEnergy

THERMAL_CORRECTION_TO_ENERGY = {"units": "kcal/mol", "name": "thermal_correction_to_energy", "value": 15.033}


class ThermalCorrectionToEnergyTest(UnitTestBase):
    def setUp(self):
        super(ThermalCorrectionToEnergyTest, self).setUp()

    def tearDown(self):
        super(ThermalCorrectionToEnergyTest, self).tearDown()

    def test_thermal_correction_to_energy(self):
        parser = self.get_mocked_parser("thermal_correction_to_energy", 15.033)
        property_ = ThermalCorrectionToEnergy("thermal_correction_to_energy", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), THERMAL_CORRECTION_TO_ENERGY)
