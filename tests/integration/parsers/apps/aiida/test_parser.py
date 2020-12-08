from tests.integration import IntegrationTestBase
from express.parsers.apps.aiida.parser import AiidaArchiveParser


class TestAiidaArchiveParser(IntegrationTestBase):

    def setUp(self):
        super(TestAiidaArchiveParser, self).setUp()
        self.parser = AiidaArchiveParser(workDir=self.workDir)

    def test_aiida_num_structures(self):
        self.assertEqual(len(self.parser.structures()), 39)

    def test_aiida_expected_keys(self):
        structures = self.parser.structures()
        for structure in self.parser.structures():
            for key in ('basis', 'lattice'):
                self.assertIn(key, structure)
