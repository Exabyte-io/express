from express.parsers.apps.vasp.parser import VaspParser

from tests.integration import ApplicationTestBase, add_tests_from_manifest
from tests.fixtures.vasp import references


@add_tests_from_manifest
class VaspTest(ApplicationTestBase):
    application = "vasp"
    parser = VaspParser
    references = references.REFERENCE_VALUES
