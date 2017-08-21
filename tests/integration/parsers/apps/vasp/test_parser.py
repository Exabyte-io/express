from tests.integration import IntegrationTestBase
from express.parsers.apps.vasp.parser import VaspParser


class TestVaspParser(IntegrationTestBase):
    def setUp(self):
        super(TestVaspParser, self).setUp()
        self.parser = VaspParser(work_dir=self.workDir, stdout_file=self.stdoutFile)

    def tearDown(self):
        super(TestVaspParser, self).setUp()

    def test_vasp_total_energy(self):
        self.assertAlmostEqual(self.parser.total_energy(), -8.208, places=2)

    def test_vasp_fermi_energy(self):
        self.assertAlmostEqual(self.parser.fermi_energy(), 3.209, places=2)

    def test_vasp_pressure(self):
        self.assertAlmostEqual(self.parser.pressure(), -93.51, places=2)
