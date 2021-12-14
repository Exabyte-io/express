from tests.fixtures.espresso.legacy_references import *
from tests.integration import IntegrationTestBase
from express.parsers.apps.espresso.parser import EspressoLegacyParser


class TestEspressoLegacyParser(IntegrationTestBase):
    def setUp(self):
        super(TestEspressoLegacyParser, self).setUp()
        self.parser = EspressoLegacyParser(work_dir=self.workDir, stdout_file=self.stdoutFile)

    def tearDown(self):
        super(TestEspressoLegacyParser, self).setUp()

    def test_espresso_eigenvalues_at_kpoints(self):
        self.assertDeepAlmostEqual(self.parser.eigenvalues_at_kpoints()[0], EIGENVALUES_AT_KPOINTS_ZERO, places=2)

    def test_espresso_ibz_k_points(self):
        self.assertDeepAlmostEqual(self.parser.ibz_k_points(), IBZ_KPOINTS, places=2)

    def test_espresso_dos(self):
        self.assertDeepAlmostEqual(self.parser.dos(), DOS, places=2)

    def test_espresso_convergence_electronic(self):
        self.assertDeepAlmostEqual(self.parser.convergence_electronic(), CONVERGENCE_ELECTRONIC, places=2)

    def test_espresso_convergence_ionic(self):
        self.assertDeepAlmostEqual(self.parser.convergence_ionic(), CONVERGENCE_IONIC, places=2)

    def test_espresso_total_energy_contributions(self):
        self.assertDeepAlmostEqual(self.parser.total_energy_contributions(), TOTAL_ENERGY_CONTRIBUTION, places=2)

    def test_espresso_phonon_dos(self):
        self.assertDeepAlmostEqual(self.parser.phonon_dos(), PHONON_DOS, places=2)

    def test_espresso_phonon_dispersion(self):
        self.assertDeepAlmostEqual(self.parser.phonon_dispersions(), PHONON_DISPERSIONS, places=2)
