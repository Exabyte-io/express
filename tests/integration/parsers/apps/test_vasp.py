from express.parsers.apps.vasp.parser import VaspParser

from tests.integration import ApplicationTestBase, add_tests
from tests.fixtures.vasp import references


@add_tests
class VaspTest(ApplicationTestBase):
    application = "vasp"
    parser = VaspParser
    references = references.REFERENCE_VALUES
