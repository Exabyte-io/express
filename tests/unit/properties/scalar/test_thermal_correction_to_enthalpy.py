from tests.unit import UnitTestBase
from express.properties.scalar.thermal_correction_to_enthalpy import ThermalCorrectionToEnthalpy

THERMAL_CORRECTION_TO_ENTHALPY = {
    "units": "kcal/mol",
    "name": "thermal_correction_to_enthalpy",
    "value": 15.626,
}


class ThermalCorrectionToEnthalpyTest(UnitTestBase):
    def setUp(self):
        super(ThermalCorrectionToEnthalpyTest, self).setUp()

    def tearDown(self):
        super(ThermalCorrectionToEnthalpyTest, self).tearDown()

    def test_thermal_correction_to_enthalpy(self):
        parser = self.get_mocked_parser("thermal_correction_to_enthalpy", 15.626)
        property_ = ThermalCorrectionToEnthalpy("thermal_correction_to_enthalpy", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), THERMAL_CORRECTION_TO_ENTHALPY)
