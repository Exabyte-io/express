# ruff: noqa: F403,F405
from express.parsers.apps.espresso.parser import EspressoParser
from tests.fixtures.espresso.v7_2.references import HUBBARD_U_PARAMS
from tests.integration import IntegrationTestBase


class TestEspressoParserV72(IntegrationTestBase):
    """
    Test espresso parser for versions 7.2, specifically parsing hp.x output.
    """
    def setUp(self):
        super(TestEspressoParserV72, self).setUp()
        self.parser = EspressoParser(work_dir=self.workDir, stdout_file=self.stdoutFile)

    def tearDown(self):
        super(TestEspressoParserV72, self).tearDown()

    def test_espresso_hubbard_u(self):
        self.assertDeepAlmostEqual(self.parser.hubbard_u(), HUBBARD_U_PARAMS, places=2)
