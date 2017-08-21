from tests.unit import UnitTestBase
from express.properties.scalar.fermi_energy import FermiEnergy

FERMI_ENERGY = {
    "units": "eV",
    "name": "fermi_energy",
    "value": 1
}


class FermiEnergyTest(UnitTestBase):
    """
    Tests fermi energy extraction.
    """

    def setUp(self):
        super(FermiEnergyTest, self).setUp()

    def tearDown(self):
        super(FermiEnergyTest, self).setUp()

    def test_fermi_energy(self):
        property_ = FermiEnergy("fermi_energy", raw_data={"fermi_energy": 1})
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), FERMI_ENERGY)
