from express.parsers.apps.vasp.parser import VaspParser

from tests.integration import IntegrationTestBase, add_tests
from tests.fixtures.vasp import references


class VaspTest(IntegrationTestBase):
    parser = VaspParser
    references = references.REFERENCE_VALUES


add_tests(VaspTest, "vasp")
