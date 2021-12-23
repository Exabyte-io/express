import os

from tests import TestBase
from tests.fixtures.structural.references import INCHI_DATA
from express.parsers.molecule import MoleculeParser


class TestMoleculeParser(TestBase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    @property
    def parser(self):
        manifest = self.manifest[self._testMethodName]
        with open(os.path.join(self.rootDir, manifest["structurePath"])) as f:
            kwargs = {
                "cell_type": manifest.get("cell_type", "original"),
                "structure_string": f.read(),
                "structure_format": "poscar"
            }
            return MoleculeParser(**kwargs)

    def test_molecule_inchi(self):
        inchi_long, self.inchi = self.parser.get_inchi()
        self.inchi_key = self.parser.get_inchi_key()
        self.assertEqual(self.inchi["value"], INCHI_DATA["inchi"])
        self.assertEqual(self.inchi_key["value"], INCHI_DATA["inchi_key"])
