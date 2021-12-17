from express.parsers.apps.espresso.parser import EspressoParser

from tests.integration import IntegrationTestBase, add_tests
from tests.fixtures.espresso import references


class EspressoTest(IntegrationTestBase):
    parser = EspressoParser
    references = references.REFERENCE_VALUES


add_tests(EspressoTest, "espresso")
