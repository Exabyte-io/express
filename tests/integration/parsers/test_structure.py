import os

from tests.fixtures.data import SI
from tests.integration import IntegrationTestBase
from express.parsers.structure import StructureParser


class TestStructureParser(IntegrationTestBase):

    def setUp(self):
        super(IntegrationTestBase, self).setUp()

    def tearDown(self):
        super(IntegrationTestBase, self).setUp()

    @property
    def parser(self):
        manifest = self.getManifest()
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
