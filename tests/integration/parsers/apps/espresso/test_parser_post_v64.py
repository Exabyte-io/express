# ruff: noqa: F403,F405
from express.parsers.apps.espresso.parser import EspressoParser
from tests.fixtures.espresso.references import *
from tests.integration import IntegrationTestBase


class TestEspressoParserPostV64(IntegrationTestBase):
    """Test espresso parser for versions > v6.4, specifically XML parser."""

    def setUp(self):
        super(TestEspressoParserPostV64, self).setUp()
        self.parser_post_v64 = EspressoParser(work_dir=self.workDir, stdout_file=self.stdoutFile, version="6.5.0")

    def tearDown(self):
        super(TestEspressoParserPostV64, self).tearDown()

    def test_espresso_fermi_energy_post_v64(self):
        self.assertAlmostEqual(self.parser_post_v64.fermi_energy(), FERMI_ENERGY_post_v64, places=2)

    def test_espresso_nspins_post_v64(self):
        self.assertEqual(self.parser_post_v64.nspins(), NSPIN)

    def test_espresso_final_lattice_vectors_post_v64(self):
        self.assertDeepAlmostEqual(self.parser_post_v64.final_lattice_vectors(), LATTICE_post_v64, places=2)

    def test_espresso_eigenvalues_at_kpoints_post_v64(self):
        self.assertDeepAlmostEqual(
            self.parser_post_v64.eigenvalues_at_kpoints()[0], EIGENVALUES_AT_KPOINTS_ZERO_post_v64, places=2
        )

    def test_espresso_eigenvalues_at_kpoints_lsda_post_v64(self):
        self.assertDeepAlmostEqual(
            self.parser_post_v64.eigenvalues_at_kpoints()[0], EIGENVALUES_AT_KPOINTS_ZERO_LSDA_post_v64, places=2
        )

    def test_espresso_final_basis_post_v64(self):
        self.assertDeepAlmostEqual(self.parser_post_v64.final_basis(), FINAL_BASIS_post_v64, places=2)
