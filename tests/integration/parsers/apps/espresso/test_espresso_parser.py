import os
from express.parsers.apps.espresso.parser import EspressoParser
import tests.fixtures.espresso.references
from tests import for_all_versions
from tests.integration import IntegrationTestBase

REFERENCE_VALUES = tests.fixtures.espresso.references.REFERENCE_VALUES

ESPRESSO_VERSIONS = {
    "6.4.1": "v641",
    "6.5.0": "v650",
    "6.6.0": "v660",
    "6.7.0": "v670",
    "6.8.0": "v680",
}

RUN_TYPES = {
    "SCF": "scf",
    "VC-Relax": "vc_relax",
}


class TestEspressoParser(IntegrationTestBase):
    def setUp(self):
        super().setUp()
        self.fixtures_dirname = os.path.dirname(tests.fixtures.espresso.references.__file__)

    def tearDown(self):
        super().tearDown()

    def _get_parser(self, version, jobtype):
        work_dir = os.path.join(self.fixtures_dirname, version, jobtype)
        stdout_file = os.path.join(work_dir, "pw.out")
        parser = EspressoParser(work_dir=work_dir, stdout_file=stdout_file)
        return parser

    for_all_espresso = for_all_versions(ESPRESSO_VERSIONS, RUN_TYPES)

    @for_all_espresso
    def test_total_energy(self, version, jobtype):
        parser = self._get_parser(version, jobtype)
        reference = REFERENCE_VALUES[version][jobtype]["total_energy"]
        result = parser.total_energy()
        self.assertAlmostEqual(reference, result, places=2)

    @for_all_espresso
    def test_fermi_energy(self, version, jobtype):
        parser = self._get_parser(version, jobtype)
        reference = REFERENCE_VALUES[version][jobtype]["fermi_energy"]
        result = parser.fermi_energy()
        self.assertAlmostEqual(reference, result, places=2)

    @for_all_espresso
    def test_pressure(self, version, jobtype):
        parser = self._get_parser(version, jobtype)
        reference = REFERENCE_VALUES[version][jobtype]["pressure"]
        result = parser.pressure()
        self.assertEqual(reference, result)

    @for_all_espresso
    def test_total_force(self, version, jobtype):
        parser = self._get_parser(version, jobtype)
        reference = REFERENCE_VALUES[version][jobtype]["total_force"]
        result = parser.total_force()
        self.assertEqual(reference, result)
