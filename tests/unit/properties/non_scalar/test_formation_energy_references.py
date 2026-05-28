from tests.unit import UnitTestBase
from express.properties.non_scalar.formation_energy_references import FormationEnergyReferencesFromContext

COMPOUND_TOTAL_ENERGY = -522.232
COMPOUND_N_ATOMS = 4
ROWS = [
    {
        "label": "SiC",
        "total_energy": COMPOUND_TOTAL_ENERGY,
        "n_atoms": COMPOUND_N_ATOMS,
        "total_energy_per_atom": COMPOUND_TOTAL_ENERGY / COMPOUND_N_ATOMS,
        "precision_value": 10,
        "precision_metric": "KPPRA",
    }
]
EXPECTED = {
    "name": "formation_energy_references",
    "value": {"rows": ROWS},
}


class FormationEnergyReferencesTest(UnitTestBase):
    def test_formation_energy_references(self):
        property_ = FormationEnergyReferencesFromContext(
            "formation_energy_references",
            None,
            value={"rows": ROWS},
        )
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), EXPECTED)
