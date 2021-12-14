from tests.fixtures.espresso.legacy_references import *
from tests.integration import IntegrationTestBase
from express.parsers.apps.espresso.parser import EspressoLegacyParser


class TestEspressoLegacyParser(IntegrationTestBase):
    def setUp(self):
        super(TestEspressoLegacyParser, self).setUp()
        self.parser = EspressoLegacyParser(work_dir=self.workDir, stdout_file=self.stdoutFile)

    def tearDown(self):
        super(TestEspressoLegacyParser, self).setUp()

    def test_espresso_phonon_dos(self):
        self.assertDeepAlmostEqual(self.parser.phonon_dos(), PHONON_DOS, places=2)

    def test_espresso_phonon_dispersion(self):
        self.assertDeepAlmostEqual(self.parser.phonon_dispersions(), PHONON_DISPERSIONS, places=2)
