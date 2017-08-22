from tests.unit import UnitTestBase
from express.properties.non_scalar.total_energy_contributions import TotalEnergyContributions

TOTAL_ENERGY_CONTRIBUTIONS = {
    "name": "total_energy_contributions",
    "ewald": {
        "name": "ewald",
        "value": 128376.45871064
    },
    "hartree": {
        "name": "hartree",
        "value": -145344.66902862
    },
    "exchangeCorrelation": {
        "name": "exchange_correlation",
        "value": 41.63693035
    },
    "units": "eV"
}


class TotalEnergyContributionsTest(UnitTestBase):
    def setUp(self):
        super(TotalEnergyContributionsTest, self).setUp()

    def tearDown(self):
        super(TotalEnergyContributionsTest, self).setUp()

    def test_atomic_forces(self):
        raw_data = {
            "total_energy_contributions": {
                "ewald": {
                    "name": "ewald",
                    "value": 128376.45871064
                },
                "hartree": {
                    "name": "hartree",
                    "value": -145344.66902862
                },
                "exchangeCorrelation": {
                    "name": "exchange_correlation",
                    "value": 41.63693035
                }
            }
        }
        property_ = TotalEnergyContributions("total_energy_contributions", raw_data=raw_data)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), TOTAL_ENERGY_CONTRIBUTIONS)
