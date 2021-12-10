import functools

from tests.integration import IntegrationTestBase
from tests.fixtures.espresso.references import REFERENCE_VALUES

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

    def tearDown(self):
        super().tearDown()

    def for_all_versions(test_function):
        @functools.wraps(test_function)
        def inner(self):
            for version_test_label, version in ESPRESSO_VERSIONS.items():
                for job_test_label, jobtype in RUN_TYPES.items():
                    with self.subTest(version_number=version_test_label, job_type=job_test_label):
                        test_function(self, version, jobtype)

        return inner
