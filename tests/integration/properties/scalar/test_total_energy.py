from express import ExPrESS

from tests.integration import IntegrationTestBase

ESPRESSO_TOTAL_ENERGY = {
    "units": "eV",
    "name": "total_energy",
    "value": -19.00890332
}

VASP_TOTAL_ENERGY = {
    "units": "eV",
    "name": "total_energy",
    "value": -8.2083074
}


class TotalEnergy(IntegrationTestBase):
    """
    Tests total energy extraction.
    """

    def setUp(self):
        super(TotalEnergy, self).setUp()

    def tearDown(self):
        super(TotalEnergy, self).setUp()

    def test_espresso_total_energy(self):
        express = ExPrESS("espresso", work_dir=self.workDir, stdout_file=self.stdoutFile)
        self.assertDeepAlmostEqual(express.property("total_energy"), ESPRESSO_TOTAL_ENERGY)

    def test_vasp_total_energy(self):
        express = ExPrESS("vasp", work_dir=self.workDir, stdout_file=self.stdoutFile)
        self.assertDeepAlmostEqual(express.property("total_energy"), VASP_TOTAL_ENERGY)
