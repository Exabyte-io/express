from express import ExPrESS

from tests.integration import IntegrationTestBase

ESPRESSO_PRESSURE = {
    "units": "kbar",
    "name": "pressure",
    "value": 73.72
}

VASP_PRESSURE = {
    "units": "kbar",
    "name": "pressure",
    "value": -93.51
}


class Pressure(IntegrationTestBase):
    """
    Tests pressure extraction.
    """

    def setUp(self):
        super(Pressure, self).setUp()

    def tearDown(self):
        super(Pressure, self).setUp()

    def test_espresso_pressure(self):
        express = ExPrESS("espresso", work_dir=self.workDir, stdout_file=self.stdoutFile)
        self.assertDeepAlmostEqual(express.property("pressure"), ESPRESSO_PRESSURE)

    def test_vasp_pressure(self):
        express = ExPrESS("vasp", work_dir=self.workDir, stdout_file=self.stdoutFile)
        self.assertDeepAlmostEqual(express.property("pressure"), VASP_PRESSURE)
