from express.parsers.apps.espresso.parser import EspressoParser

from tests.integration import ApplicationTestBase, add_tests
from tests.fixtures.espresso import references


@add_tests
class EspressoTest(ApplicationTestBase):
    application = "espresso"
    parser = EspressoParser
    references = references.REFERENCE_VALUES
