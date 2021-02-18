from tests.integration import IntegrationTestBase
from express.parsers.apps.aiida.parser import AiidaArchiveParser


class TestAiidaArchiveParser(IntegrationTestBase):

    def setUp(self):
        super(TestAiidaArchiveParser, self).setUp()
        self.parser = AiidaArchiveParser(work_dir=self.workDir)

    def test_aiida_num_structures(self):
        """
        Test number of structures parsed from fixture is as expected.

        The fixture contains 39 structures, so the number of parsed
        structures should match that number.
        """

        self.assertEqual(len(self.parser.initial_structure_strings()), 39)
