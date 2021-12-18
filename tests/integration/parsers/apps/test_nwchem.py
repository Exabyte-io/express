from express.parsers.apps.nwchem.parser import NwchemParser

from tests.integration import ApplicationTestBase, add_tests
from tests.fixtures.nwchem import references


@add_tests
class NwchemTest(ApplicationTestBase):
    application = "nwchem"
    parser = NwchemParser
    references = references.REFERENCE_VALUES
