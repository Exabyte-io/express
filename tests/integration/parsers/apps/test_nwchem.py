from express.parsers.apps.nwchem.parser import NwchemParser

from tests.integration import IntegrationTestBase, add_tests
from tests.fixtures.nwchem import references


class NwchemTest(IntegrationTestBase):
    parser = NwchemParser
    references = references.REFERENCE_VALUES


add_tests(NwchemTest, "nwchem")
