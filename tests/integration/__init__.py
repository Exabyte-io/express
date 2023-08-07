import os

from tests import TestBase


class IntegrationTestBase(TestBase):
    """
    Base class for express integration tests.
    """

    def setUp(self):
        super(IntegrationTestBase, self).setUp()

    def tearDown(self):
        super(IntegrationTestBase, self).tearDown()

    @property
    def workDir(self):
        return os.path.join(self.rootDir, self.getManifest()["workDir"])

    @property
    def stdoutFile(self):
        return os.path.join(self.rootDir, self.getManifest()["stdoutFile"])
