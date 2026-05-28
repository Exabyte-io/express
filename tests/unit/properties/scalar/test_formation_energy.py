from tests.unit import UnitTestBase
from express.properties.scalar.scalar_property_context import ScalarPropertyFromContext

FORMATION_ENERGY = {"units": "eV/atom", "name": "formation_energy", "value": -0.123}
FORMATION_ENERGY_VALUE = -0.123


class FormationEnergyTest(UnitTestBase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_formation_energy(self):
        parser = self.get_mocked_parser("formation_energy", FORMATION_ENERGY_VALUE)  # noqa : F841
        property_ = ScalarPropertyFromContext("formation_energy", None, value=FORMATION_ENERGY_VALUE)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), FORMATION_ENERGY)
