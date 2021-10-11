import os

from tests.fixtures.data import SI
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
                "structure_string": f.read(),
                "cell": manifest.get("cell", "original"),
                "structure_format": manifest.get("structureFormat", "poscar")
            }
            return CrystalParser(**kwargs)

    def test_crystal_espresso_lattice_bravais(self):
        self.assertDeepAlmostEqual(self.parser.lattice_bravais(), SI["lattice"], places=2)

    def test_crystal_vasp_lattice_bravais(self):
        self.assertDeepAlmostEqual(self.parser.lattice_bravais(), SI["lattice"], places=2)
