import os

from tests import TestBase, settings


class IntegrationTestBase(TestBase):
    """
    Base class for express integration tests.
    """

    def setUp(self):
        super(IntegrationTestBase, self).setUp()
        self.workDir = os.path.join(self.rootDir, self.getManifest()["workDir"])
        self.stdoutFile = os.path.join(self.rootDir, self.getManifest()["stdoutFile"])
        if settings.RERUN_TEST:
            os.system("cd {}; sh run.sh".format(self.workDir))

    def tearDown(self):
        super(IntegrationTestBase, self).setUp()
