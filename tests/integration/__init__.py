from tests import TestBase


class IntegrationTestBase(TestBase):
    """
    Base class for express integration tests.
    """

    def setUp(self):
        super(IntegrationTestBase, self).setUp()

    def tearDown(self):
        super(IntegrationTestBase, self).setUp()
