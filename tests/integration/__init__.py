import os

from tests import TestBase


class IntegrationTestBase(TestBase):
    """
    Base class for express integration tests.
    """

    def setUp(self):
        super(IntegrationTestBase, self).setUp()

    def tearDown(self):
        super(IntegrationTestBase, self).setUp()

    @property
    def workDir(self):
        return os.path.join(self.rootDir, self.manifest[self._testMethodName]["workDir"])

    @property
    def stdoutFile(self):
        return os.path.join(self.rootDir, self.manifest[self._testMethodName]["stdoutFile"])
