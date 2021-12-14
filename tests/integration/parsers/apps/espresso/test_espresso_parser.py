import os
import yaml
from express.parsers.apps.espresso.parser import EspressoParser, EspressoLegacyParser
import tests.fixtures.espresso.references
from tests import for_all_versions, TestBase
from tests import __file__ as base_test_file_path
from tests.integration import IntegrationTestBase

REFERENCE_VALUES = tests.fixtures.espresso.references.REFERENCE_VALUES

manifest_path = os.path.join(os.path.dirname(base_test_file_path), "manifest.yaml")
with open(manifest_path, "r") as fp:
    test_yaml = yaml.load(fp)
espresso_configs = test_yaml['applications']['espresso']

class TestEspressoParser(IntegrationTestBase):
    def setUp(self):
        super().setUp()
        self.fixtures_dirname = os.path.dirname(tests.fixtures.espresso.references.__file__)

    def tearDown(self):
        super().tearDown()

    def _get_parser(self, version, runtype):
        work_dir = os.path.join(self.fixtures_dirname, version, runtype)
        if version == "v540":
            parser_cls = EspressoLegacyParser
            stdout_file = os.path.join(work_dir, f"pw-{runtype}.out")
        else:
            parser_cls = EspressoParser
            stdout_file = os.path.join(work_dir, "pw.out")
        parser = parser_cls(work_dir=work_dir, stdout_file=stdout_file)
        return parser

    for_all_espresso = for_all_versions(espresso_configs)

    # ===============================================================
    # Basic functionality that all versions should be able to handle
    # ===============================================================
    @for_all_espresso
    def test_total_energy(self, version, runtype, test_config):
        fixture_dir = test_config['base_dir']
        parser = self._get_parser(fixture_dir, runtype)
        reference = REFERENCE_VALUES[fixture_dir][runtype]["total_energy"]
        if reference != "NOT_TESTED":
            result = parser.total_energy()
            self.assertAlmostEqual(reference, result, places=2)

    @for_all_espresso
    def test_fermi_energy(self, version, runtype, test_config):
        fixture_dir = test_config['base_dir']
        parser = self._get_parser(fixture_dir, runtype)
        reference = REFERENCE_VALUES[fixture_dir][runtype]["fermi_energy"]
        if reference != "NOT_TESTED":
            result = parser.fermi_energy()
            self.assertAlmostEqual(reference, result, places=2)

    @for_all_espresso
    def test_nspin(self, version, runtype, test_config):
        fixture_dir = test_config['base_dir']
        parser = self._get_parser(fixture_dir, runtype)
        reference = REFERENCE_VALUES[fixture_dir][runtype]["nspin"]
        if reference != "NOT_TESTED":
            result = parser.nspins()
            self.assertEqual(reference, result)

    # eigenvalues_at_kpoints

    # ibz_k_points

    # dos

    # convergence_electronic

    # convergence_ionic

    # stress_tensor

    @for_all_espresso
    def test_pressure(self, version, runtype, test_config):
        fixture_dir = test_config['base_dir']
        parser = self._get_parser(fixture_dir, runtype)
        reference = REFERENCE_VALUES[fixture_dir][runtype]["pressure"]
        if reference != "NOT_TESTED":
            result = parser.pressure()
            self.assertEqual(reference, result)

    @for_all_espresso
    def test_final_realspace_lattice_vectors(self, version, runtype, test_config):
        fixture_dir = test_config['base_dir']
        parser = self._get_parser(fixture_dir, runtype)
        reference = REFERENCE_VALUES[fixture_dir][runtype]["realspace_lattice"]
        if reference != "NOT_TESTED":
            result = parser.final_lattice_vectors()
            self.assertDeepAlmostEqual(expected=reference, actual=result, places=3)

    @for_all_espresso
    def test_final_reciprocal_lattice_vectors(self, version, runtype, test_config):
        fixture_dir = test_config['base_dir']
        parser = self._get_parser(fixture_dir, runtype)
        reference = REFERENCE_VALUES[fixture_dir][runtype]["reciprocal_lattice"]
        if reference != "NOT_TESTED":
            result = parser.xml_parser.final_lattice_vectors(reciprocal=True)
            self.assertDeepAlmostEqual(expected=reference, actual=result)

    # total_force

    # atomic_forces

    # energy_contributions

    # phonon_dos

    # phonon_dispersion
