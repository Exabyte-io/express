# ruff: noqa: F403,F405
from express.parsers.apps.vasp.parser import VaspParser
from tests.fixtures.vasp.references import *
from tests.integration import IntegrationTestBase


class TestVaspParser(IntegrationTestBase):
    def setUp(self):
        super(TestVaspParser, self).setUp()
        self.parser = VaspParser(work_dir=self.workDir, stdout_file=self.stdoutFile)

    def tearDown(self):
        super(TestVaspParser, self).tearDown()

    def test_vasp_total_energy(self):
        self.assertAlmostEqual(self.parser.total_energy(), TOTAL_ENERGY, places=2)

    def test_vasp_fermi_energy(self):
        self.assertAlmostEqual(self.parser.fermi_energy(), FERMI_ENERGY, places=2)

    def test_vasp_nspins(self):
        self.assertEqual(self.parser.nspins(), NSPIN)

    def test_vasp_eigenvalues_at_kpoints(self):
        self.assertDeepAlmostEqual(self.parser.eigenvalues_at_kpoints()[0], EIGENVALUES_AT_KPOINTS_ZERO, places=2)

    def test_vasp_ibz_k_points(self):
        self.assertDeepAlmostEqual(self.parser.ibz_k_points(), IBZ_KPOINTS, places=2)

    def test_vasp_dos(self):
        self.assertDeepAlmostEqual(self.parser.dos(), DOS)

    def test_vasp_convergence_electronic(self):
        self.assertDeepAlmostEqual(self.parser.convergence_electronic(), CONVERGENCE_ELECTRONIC, places=2)

    def test_vasp_convergence_ionic(self):
        self.assertDeepAlmostEqual(self.parser.convergence_ionic(), CONVERGENCE_IONIC, places=2)

    def test_vasp_stress_tensor(self):
        self.assertDeepAlmostEqual(self.parser.stress_tensor(), STRESS_TENSOR, places=2)

    def test_vasp_pressure(self):
        self.assertAlmostEqual(self.parser.pressure(), PRESSURE, places=2)

    def test_vasp_total_force(self):
        self.assertAlmostEqual(self.parser.total_force(), TOTAL_FORCE, places=2)

    def test_vasp_atomic_forces(self):
        self.assertDeepAlmostEqual(self.parser.atomic_forces(), ATOMIC_FORCES, places=2)

    def test_vasp_total_energy_contributions(self):
        self.assertDeepAlmostEqual(self.parser.total_energy_contributions(), TOTAL_ENERGY_CONTRIBUTION, places=2)

    def test_vasp_magnetic_moments(self):
        self.assertDeepAlmostEqual(self.parser.magnetic_moments(), MAGNETIC_MOMENTS, places=3)
