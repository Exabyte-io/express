import os

from tests.fixtures.structural.references import INCHI_DATA
from tests.fixtures.structural.references import POINT_GROUP_DATA
from tests.integration import IntegrationTestBase
from express.parsers.molecule import MoleculeParser


class TestMoleculeParser(IntegrationTestBase):

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
                "is_non_periodic": True
            }
            return MoleculeParser(**kwargs)

    def test_molecule_inchi(self):
        inchi_long, self.inchi = self.parser.get_inchi()
        self.inchi_key = self.parser.get_inchi_key()
        self.assertEqual(self.inchi["value"], INCHI_DATA["inchi"])
        self.assertEqual(self.inchi_key["value"], INCHI_DATA["inchi_key"])

    def test_molecule_point_group_symmetry(self):
        self.point_group_symmetry = self.parser.point_group_symbol()
        self.assertEqual(self.point_group_symmetry['value'], POINT_GROUP_DATA["value"])
