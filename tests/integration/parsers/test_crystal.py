import os

from tests.fixtures.structural.references import SPACE_GROUP_DATA
from tests.integration import IntegrationTestBase
from express.parsers.crystal import CrystalParser


class TestCrystalParser(IntegrationTestBase):

    def setUp(self):
        super(IntegrationTestBase, self).setUp()

    def tearDown(self):
        super(IntegrationTestBase, self).setUp()

    @property
    def parser(self):
        manifest = self.getManifest()
        with open(os.path.join(self.rootDir, manifest["structurePath"])) as f:
            kwargs = {
                "cell_type": manifest.get("cell_type", "original"),
                "structure_string": f.read(),
                "structure_format": "poscar",
                "is_non_periodic": False
            }
            return CrystalParser(**kwargs)

    def test_crystal_space_group_symmetry(self):
        self.space_group_symmetry = self.parser.space_group_symbol()
        print(self.space_group_symmetry)
        self.assertEqual(self.space_group_symmetry['value'], SPACE_GROUP_DATA["value"])
