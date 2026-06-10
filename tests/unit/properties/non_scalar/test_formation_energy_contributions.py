from tests.unit import UnitTestBase

from express.properties.non_scalar.non_scalar_property_context import NonScalarPropertyFromContext

COMPOUND_CONTRIBUTION = {
    "formula": "SiC",
    "n_atoms": 4,
    "is_elemental": False,
    "total_energy": -520.003969643439,
    "total_energy_per_atom": -130.00099241085975,
    "precision_value": 8192,
    "precision_metric": "KPPRA",
}
SILICON_CONTRIBUTION = {
    "formula": "Si",
    "n_atoms": 2,
    "is_elemental": True,
    "total_energy": -261.003969643439,
    "total_energy_per_atom": -130.5019848217195,
    "precision_value": 8192,
    "precision_metric": "KPPRA",
}
FORMATION_ENERGY_CONTRIBUTIONS_VALUES = [COMPOUND_CONTRIBUTION, SILICON_CONTRIBUTION]
FORMATION_ENERGY_CONTRIBUTIONS = {
    "name": "formation_energy_contributions",
    "values": FORMATION_ENERGY_CONTRIBUTIONS_VALUES,
}


class FormationEnergyContributionsTest(UnitTestBase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_formation_energy_contributions_from_context_values(self):
        property_ = NonScalarPropertyFromContext(
            "formation_energy_contributions",
            None,
            data=FORMATION_ENERGY_CONTRIBUTIONS_VALUES,
        )

        self.assertDeepAlmostEqual(property_.serialize_and_validate(), FORMATION_ENERGY_CONTRIBUTIONS)

    def test_formation_energy_contributions_from_context_data(self):
        property_ = NonScalarPropertyFromContext(
            "formation_energy_contributions",
            None,
            data={"values": FORMATION_ENERGY_CONTRIBUTIONS_VALUES},
        )

        self.assertDeepAlmostEqual(property_.serialize_and_validate(), FORMATION_ENERGY_CONTRIBUTIONS)

    def test_formation_energy_contributions_from_value_alias(self):
        property_ = NonScalarPropertyFromContext(
            "formation_energy_contributions",
            None,
            value=FORMATION_ENERGY_CONTRIBUTIONS_VALUES,
        )

        self.assertDeepAlmostEqual(property_.serialize_and_validate(), FORMATION_ENERGY_CONTRIBUTIONS)

    def test_formation_energy_contributions_from_context_key(self):
        property_ = NonScalarPropertyFromContext(
            "formation_energy_contributions",
            None,
            context={"FORMATION_ENERGY_REFERENCES": FORMATION_ENERGY_CONTRIBUTIONS_VALUES},
            context_key="FORMATION_ENERGY_REFERENCES",
        )

        self.assertDeepAlmostEqual(property_.serialize_and_validate(), FORMATION_ENERGY_CONTRIBUTIONS)
