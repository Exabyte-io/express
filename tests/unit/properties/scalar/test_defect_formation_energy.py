from tests.unit import UnitTestBase
from express.properties.scalar.scalar_property_context import ScalarPropertyFromContext

DEFECT_FORMATION_ENERGY = {"units": "eV/defect", "name": "defect_formation_energy", "value": 3.5}


class DefectFormationEnergyTest(UnitTestBase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_defect_formation_energy(self):
        property_ = ScalarPropertyFromContext(
            "defect_formation_energy", None, value=DEFECT_FORMATION_ENERGY["value"]
        )
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), DEFECT_FORMATION_ENERGY)
