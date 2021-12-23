from express.parsers.apps.espresso.parser import EspressoParser

from tests.integration import ApplicationTestBase, add_tests_from_manifest
from tests.fixtures.espresso import references


@add_tests_from_manifest
class EspressoTest(ApplicationTestBase):
    application = "espresso"
    parser = EspressoParser
    references = references.REFERENCE_VALUES
