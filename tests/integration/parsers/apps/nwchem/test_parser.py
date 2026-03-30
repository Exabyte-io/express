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

    def test_nwchem_homo_energy(self):
        self.assertAlmostEqual(self.parser.homo_energy(), HOMO_ENERGY, places=2)

    def test_nwchem_lumo_energy(self):
        self.assertAlmostEqual(self.parser.lumo_energy(), LUMO_ENERGY, places=2)

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
