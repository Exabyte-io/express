import os

from tests import TestBase
from tests.fixtures.data import SI
from express.parsers.structure import StructureParser


class TestStructureParser(TestBase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().setUp()

    @property
    def parser(self):
        manifest = self.manifest[self._testMethodName]
        with open(os.path.join(self.rootDir, manifest["structurePath"])) as f:
            kwargs = {
                "structure_string": f.read(),
                "cell_type": manifest.get("cell_type", "original"),
                "structure_format": manifest.get("structureFormat", "poscar")
            }
            return StructureParser(**kwargs)

    def test_structure_espresso_basis(self):
        self.assertDeepAlmostEqual(self.parser.basis(), SI["basis"], places=2)

    def test_structure_vasp_basis(self):
        self.assertDeepAlmostEqual(self.parser.basis(), SI["basis"], places=2)

    def test_structure_espresso_lattice_bravais(self):
        self.assertDeepAlmostEqual(self.parser.lattice_bravais(), SI["lattice"], places=2)

    def test_structure_vasp_lattice_bravais(self):
        self.assertDeepAlmostEqual(self.parser.lattice_bravais(), SI["lattice"], places=2)
