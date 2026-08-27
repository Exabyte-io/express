# ruff: noqa: F403,F405
from express.parsers.apps.nwchem.parser import NwchemParser
from tests.fixtures.nwchem.references import *
from tests.integration import IntegrationTestBase


class TestNwchemParser(IntegrationTestBase):
    def setUp(self):
        super(TestNwchemParser, self).setUp()
        self.parser = NwchemParser(work_dir=self.workDir, stdout_file=self.stdoutFile)

    def tearDown(self):
        super(TestNwchemParser, self).tearDown()

    def test_nwchem_total_energy(self):
        self.assertAlmostEqual(self.parser.total_energy(), TOTAL_ENERGY, places=2)

    def test_nwchem_eigenvalues_at_vectors(self):
        eigenvalues = self.parser.eigenvalues_at_vectors()
        self.assertEqual(len(eigenvalues), EIGENVALUES_AT_VECTORS_COUNT)
        self.assertDeepAlmostEqual(eigenvalues[0], EIGENVALUES_AT_VECTORS_FIRST, places=2)
        self.assertDeepAlmostEqual(eigenvalues[-1], EIGENVALUES_AT_VECTORS_LAST, places=2)

    def test_nwchem_eigenvalues_at_vectors_multistep(self):
        eigenvalues = self.parser.eigenvalues_at_vectors()
        self.assertEqual(len(eigenvalues), EIGENVALUES_AT_VECTORS_MULTISTEP_COUNT)
        self.assertDeepAlmostEqual(eigenvalues[0], EIGENVALUES_AT_VECTORS_MULTISTEP_FIRST, places=2)
        self.assertDeepAlmostEqual(eigenvalues[-1], EIGENVALUES_AT_VECTORS_MULTISTEP_LAST, places=2)

    def test_nwchem_homo_energy(self):
        homo_energy = self.parser.homo_energy()
        self.assertAlmostEqual(homo_energy, HOMO_ENERGY, places=2)
        self.assertNotAlmostEqual(homo_energy, HOMO_ENERGY_INITIAL_GUESS, places=2)

    def test_nwchem_lumo_energy(self):
        lumo_energy = self.parser.lumo_energy()
        self.assertAlmostEqual(lumo_energy, LUMO_ENERGY, places=2)
        self.assertNotAlmostEqual(lumo_energy, LUMO_ENERGY_INITIAL_GUESS, places=2)

    def test_nwchem_homo_energy_multistep(self):
        homo_energy = self.parser.homo_energy()
        self.assertAlmostEqual(homo_energy, HOMO_ENERGY_MULTISTEP, places=2)
        self.assertNotAlmostEqual(homo_energy, HOMO_ENERGY_MULTISTEP_INITIAL_GUESS, places=2)

    def test_nwchem_lumo_energy_multistep(self):
        lumo_energy = self.parser.lumo_energy()
        self.assertAlmostEqual(lumo_energy, LUMO_ENERGY_MULTISTEP, places=2)
        self.assertNotAlmostEqual(lumo_energy, LUMO_ENERGY_MULTISTEP_INITIAL_GUESS, places=2)

    def test_nwchem_structures_of_single_point(self):
        self.assertDeepAlmostEqual(self.parser.initial_basis(), BASIS, places=6)
        self.assertDeepAlmostEqual(self.parser.final_basis(), BASIS, places=6)

    def test_nwchem_total_energy_contributions(self):
        self.assertDeepAlmostEqual(self.parser.total_energy_contributions(), TOTAL_ENERGY_CONTRIBUTION, places=2)

    def test_nwchem_zero_point_energy(self):
        self.assertAlmostEqual(self.parser.zero_point_energy(), ZERO_POINT_ENERGY, places=2)

    def test_nwchem_thermal_correction_to_energy(self):
        self.assertAlmostEqual(self.parser.thermal_correction_to_energy(), THERMAL_CORRECTION_TO_ENERGY, places=2)

    def test_nwchem_thermal_correction_to_enthalpy(self):
        self.assertAlmostEqual(
            self.parser.thermal_correction_to_enthalpy(), THERMAL_CORRECTION_TO_ENTHALPY, places=2
        )
