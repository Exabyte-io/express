import os

from tests import TestBase


class IntegrationTestBase(TestBase):
    """
    Base class for express integration tests.
    """

    def setUp(self):
        super(IntegrationTestBase, self).setUp()
        self.workDir = os.path.join(self.rootDir, self.getManifest()["workDir"])
        self.stdoutFile = os.path.join(self.rootDir, self.getManifest()["stdoutFile"])

    def tearDown(self):
        super(IntegrationTestBase, self).setUp()
