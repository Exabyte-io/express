from tests.integration import IntegrationTestBase
from express.parsers.apps.aiida.parser import AiidaArchiveParser


class TestAiidaArchiveParser(IntegrationTestBase):

    def setUp(self):
        super(TestAiidaArchiveParser, self).setUp()
        self.parser = AiidaArchiveParser(workDir=self.workDir)

    def test_aiida_num_structures(self):
        """
        Test number of structures parsed from fixture is as expected.

        The fixture contains 39 structures, so the number of parsed
        structures should match that number.
        """

        self.assertEqual(len(self.parser.structures()), 39)

    def test_aiida_expected_keys(self):
        """
        Test that all structures parsed from fixture have expected keys.

        All structures parsed from the fixture should contain at least
        a unit cell definition via 'basis' and 'lattice' vectors.
        """

        structures = self.parser.structures()
        for structure in self.parser.structures():
            for key in ('basis', 'lattice'):
                self.assertIn(key, structure)
