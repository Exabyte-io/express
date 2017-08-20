from express import ExPrESS

from tests.integration import IntegrationTestBase

ESPRESSO_FERMI_ENERGY = {
    "units": "eV",
    "name": "fermi_energy",
    "value": 6.6078556811104292
}

VASP_FERMI_ENERGY = {
    "units": "eV",
    "name": "fermi_energy",
    "value": 3.20903016
}


class FermiEnergy(IntegrationTestBase):
    """
    Tests fermi energy extraction.
    """

    def setUp(self):
        super(FermiEnergy, self).setUp()

    def tearDown(self):
        super(FermiEnergy, self).setUp()

    def test_espresso_fermi_energy(self):
        express = ExPrESS("espresso", work_dir=self.workDir, stdout_file=self.stdoutFile)
        self.assertDeepAlmostEqual(express.property("fermi_energy"), ESPRESSO_FERMI_ENERGY)

    def test_vasp_fermi_energy(self):
        express = ExPrESS("vasp", work_dir=self.workDir, stdout_file=self.stdoutFile)
        self.assertDeepAlmostEqual(express.property("fermi_energy"), VASP_FERMI_ENERGY)
