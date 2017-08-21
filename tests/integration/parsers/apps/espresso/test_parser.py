from tests.integration import IntegrationTestBase
from express.parsers.apps.espresso.parser import EspressoParser


class TestEspressoParser(IntegrationTestBase):
    def setUp(self):
        super(TestEspressoParser, self).setUp()
        self.parser = EspressoParser(work_dir=self.workDir, stdout_file=self.stdoutFile)

    def tearDown(self):
        super(TestEspressoParser, self).setUp()

    def test_espresso_total_energy(self):
        self.assertAlmostEqual(self.parser.total_energy(), -19.008, places=2)

    def test_espresso_fermi_energy(self):
        self.assertAlmostEqual(self.parser.fermi_energy(), 6.607, places=2)

    def test_espresso_pressure(self):
        self.assertAlmostEqual(self.parser.pressure(), 73.72, places=2)
