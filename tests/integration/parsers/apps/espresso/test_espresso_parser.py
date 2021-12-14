import os
import yaml
from express.parsers.apps.espresso.parser import EspressoParser, EspressoLegacyParser
import tests.fixtures.espresso.references
from tests import for_all_versions
from tests import __file__ as base_test_file_path
from tests.integration import IntegrationTestBase

REFERENCE_VALUES = tests.fixtures.espresso.references.REFERENCE_VALUES
LEGACY_REFERENCE_VALUES = tests.fixtures.espresso.references.LEGACY_REFERENCE_VALUES

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

    def _get_parser_and_reference(self, runtype, test_config, target_property):
        fixture_dir = test_config['base_dir']
        parser = self._get_parser(fixture_dir, runtype)
        reference = REFERENCE_VALUES[fixture_dir][runtype][target_property]
        return parser, reference

    @for_all_espresso
    def test_total_energy(self, runtype, test_config):
        test_property = "total_energy"
        parser, reference = self._get_parser_and_reference(runtype, test_config, test_property)
        if reference != "NOT_TESTED":
            result = parser.total_energy()
            self.assertAlmostEqual(reference, result, places=2)

    @for_all_espresso
    def test_fermi_energy(self, runtype, test_config):
        test_property = "fermi_energy"
        parser, reference = self._get_parser_and_reference(runtype, test_config, test_property)
        if reference != "NOT_TESTED":
            result = parser.fermi_energy()
            self.assertAlmostEqual(reference, result, places=2)

    @for_all_espresso
    def test_nspin(self, runtype, test_config):
        test_property = "nspin"
        parser, reference = self._get_parser_and_reference(runtype, test_config, test_property)
        if reference != "NOT_TESTED":
            result = parser.nspins()
            self.assertEqual(reference, result)

    @for_all_espresso
    def test_eigenvalues_at_kpoints(self, runtype, test_config):
        test_property = "eigenvalues_at_kpoints"
        parser, reference = self._get_parser_and_reference(runtype, test_config, test_property)
        if reference != "NOT_TESTED":
            result = parser.eigenvalues_at_kpoints()
            # This test is a special case, because only the first eigenvalue was historically checked
            first_kpoint_result = result[0]
            self.assertDeepAlmostEqual(reference, first_kpoint_result)

    @for_all_espresso
    def test_ibz_k_points(self, runtype, test_config):
        test_property = "ibz_k_points"
        parser, reference = self._get_parser_and_reference(runtype, test_config, test_property)
        if reference != "NOT_TESTED":
            result = parser.ibz_k_points()
            self.assertDeepAlmostEqual(reference, result)

    @for_all_espresso
    def test_convergence_electronic(self, runtype, test_config):
        test_property = "convergence_electronic"
        parser, reference = self._get_parser_and_reference(runtype, test_config, test_property)
        if reference != "NOT_TESTED":
            result = parser.convergence_electronic()
            self.assertDeepAlmostEqual(reference, result)

    @for_all_espresso
    def test_convergence_ionic(self, runtype, test_config):
        test_property = "convergence_ionic"
        parser, reference = self._get_parser_and_reference(runtype, test_config, test_property)
        if reference != "NOT_TESTED":
            result = parser.convergence_ionic()
            self.assertDeepAlmostEqual(reference, result)

    @for_all_espresso
    def test_stress_tensor(self, runtype, test_config):
        test_property = "stress_tensor"
        parser, reference = self._get_parser_and_reference(runtype, test_config, test_property)
        if reference != "NOT_TESTED":
            result = parser.stress_tensor()
            self.assertDeepAlmostEqual(reference, result)

    @for_all_espresso
    def test_pressure(self, runtype, test_config):
        test_property = "pressure"
        parser, reference = self._get_parser_and_reference(runtype, test_config, test_property)
        if reference != "NOT_TESTED":
            result = parser.pressure()
            self.assertEqual(reference, result)

    @for_all_espresso
    def test_final_realspace_lattice_vectors(self, runtype, test_config):
        test_property = "realspace_lattice"
        parser, reference = self._get_parser_and_reference(runtype, test_config, test_property)
        if reference != "NOT_TESTED":
            result = parser.final_lattice_vectors()
            self.assertDeepAlmostEqual(expected=reference, actual=result, places=3)

    @for_all_espresso
    def test_final_reciprocal_lattice_vectors(self, runtype, test_config):
        test_property = "reciprocal_lattice"
        parser, reference = self._get_parser_and_reference(runtype, test_config, test_property)
        if reference != "NOT_TESTED":
            result = parser.xml_parser.final_lattice_vectors(reciprocal=True)
            self.assertDeepAlmostEqual(expected=reference, actual=result)

    @for_all_espresso
    def test_total_force(self, runtype, test_config):
        test_property = "total_force"
        parser, reference = self._get_parser_and_reference(runtype, test_config, test_property)
        if reference != "NOT_TESTED":
            result = parser.total_force()
            self.assertEqual(reference, result)

    @for_all_espresso
    def test_atomic_forces(self, runtype, test_config):
        test_property = "atomic_forces"
        parser, reference = self._get_parser_and_reference(runtype, test_config, test_property)
        if reference != "NOT_TESTED":
            result = parser.atomic_forces()
            self.assertDeepAlmostEqual(reference, result)

    @for_all_espresso
    def test_total_energy_contributions(self, runtype, test_config):
        test_property = "total_energy_contributions"
        parser, reference = self._get_parser_and_reference(runtype, test_config, test_property)
        if reference != "NOT_TESTED":
            result = parser.total_energy_contributions()
            self.assertDeepAlmostEqual(reference, result)

    # =============================================
    # Legacy test cases that had specific fixtures
    # =============================================

    def test_legacy_dos(self):
        with self.subTest(version="5.4.0"):
            version = "v540"
            reference = LEGACY_REFERENCE_VALUES["dos"]

            work_dir = os.path.join(self.fixtures_dirname, version, "dos")
            stdout_file = os.path.join(work_dir, "pw-projwfc.out")
            parser = EspressoLegacyParser(work_dir=work_dir, stdout_file=stdout_file)
            result = parser.dos()

            self.assertDeepAlmostEqual(reference, result)

    def test_legacy_phonon_dos(self):
        with self.subTest(version="5.4.0"):
            version = "v540"
            reference = LEGACY_REFERENCE_VALUES["phonon_dos"]

            work_dir = os.path.join(self.fixtures_dirname, version, "phonon_dos")
            stdout_file = os.path.join(work_dir, "phonon_dos.out")
            parser = EspressoLegacyParser(work_dir=work_dir, stdout_file=stdout_file)
            result = parser.phonon_dos()

            self.assertDeepAlmostEqual(reference, result)

    def test_legacy_phonon_dispersion(self):
        with self.subTest(version="5.4.0"):
            version = "v540"
            reference = LEGACY_REFERENCE_VALUES["phonon_dispersions"]

            work_dir = os.path.join(self.fixtures_dirname, version, "phonon_dos")
            stdout_file = os.path.join(work_dir, "normal_modes.out")
            parser = EspressoLegacyParser(work_dir=work_dir, stdout_file=stdout_file)
            result = parser.phonon_dispersions()

            self.assertDeepAlmostEqual(reference, result)
