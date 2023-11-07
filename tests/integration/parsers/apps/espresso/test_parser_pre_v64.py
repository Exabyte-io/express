# ruff: noqa: F403,F405
from express.parsers.apps.espresso.parser import EspressoParser
from tests.fixtures.espresso.references import *
from tests.integration import IntegrationTestBase


class TestEspressoParserPreV64(IntegrationTestBase):
    def setUp(self):
        super(TestEspressoParserPreV64, self).setUp()
        self.parser_pre_v64 = EspressoParser(work_dir=self.workDir, stdout_file=self.stdoutFile)

    def tearDown(self):
        super(TestEspressoParserPreV64, self).tearDown()

    def test_espresso_total_energy(self):
        self.assertAlmostEqual(self.parser_pre_v64.total_energy(), TOTAL_ENERGY, places=2)

    def test_espresso_ibz_k_points(self):
        self.assertDeepAlmostEqual(self.parser_pre_v64.ibz_k_points(), IBZ_KPOINTS, places=2)

    def test_espresso_dos(self):
        self.assertDeepAlmostEqual(self.parser_pre_v64.dos(), DOS, places=2)

    def test_espresso_convergence_electronic(self):
        self.assertDeepAlmostEqual(self.parser_pre_v64.convergence_electronic(), CONVERGENCE_ELECTRONIC, places=2)

    def test_espresso_convergence_ionic(self):
        self.assertDeepAlmostEqual(self.parser_pre_v64.convergence_ionic(), CONVERGENCE_IONIC, places=2)

    def test_espresso_stress_tensor(self):
        self.assertDeepAlmostEqual(self.parser_pre_v64.stress_tensor(), STRESS_TENSOR, places=2)

    def test_espresso_pressure(self):
        self.assertAlmostEqual(self.parser_pre_v64.pressure(), PRESSURE, places=2)

    def test_espresso_total_force(self):
        self.assertAlmostEqual(self.parser_pre_v64.total_force(), TOTAL_FORCE, places=2)

    def test_espresso_atomic_forces(self):
        self.assertDeepAlmostEqual(self.parser_pre_v64.atomic_forces(), ATOMIC_FORCES, places=2)

    def test_espresso_total_energy_contributions(self):
        self.assertDeepAlmostEqual(
            self.parser_pre_v64.total_energy_contributions(), TOTAL_ENERGY_CONTRIBUTION, places=2
        )

    def test_espresso_phonon_dos(self):
        self.assertDeepAlmostEqual(self.parser_pre_v64.phonon_dos(), PHONON_DOS, places=2)

    def test_espresso_phonon_dispersion(self):
        self.assertDeepAlmostEqual(self.parser_pre_v64.phonon_dispersions(), PHONON_DISPERSIONS, places=2)

    # XML version dependent tests
    def test_espresso_fermi_energy_pre_v64(self):
        self.assertAlmostEqual(self.parser_pre_v64.fermi_energy(), FERMI_ENERGY, places=2)

    def test_espresso_nspins_pre_v64(self):
        self.assertEqual(self.parser_pre_v64.nspins(), NSPIN)

    def test_espresso_final_lattice_vectors_pre_v64(self):
        self.assertDeepAlmostEqual(self.parser_pre_v64.final_lattice_vectors(), LATTICE, places=2)

    def test_espresso_eigenvalues_at_kpoints_pre_v64(self):
        self.assertDeepAlmostEqual(
            self.parser_pre_v64.eigenvalues_at_kpoints()[0], EIGENVALUES_AT_KPOINTS_ZERO, places=2
        )
