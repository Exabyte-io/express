from unittest.mock import MagicMock

from tests import TestBase


class UnitTestBase(TestBase):
    """
    Base class for express unit tests.
    """

    def setUp(self):
        super(UnitTestBase, self).setUp()

    def tearDown(self):
        super(UnitTestBase, self).tearDown()

    def get_mocked_parser(self, method_name, return_value):
        parser = MagicMock()
        parser.attach_mock(MagicMock(return_value=return_value), method_name)
        return parser
