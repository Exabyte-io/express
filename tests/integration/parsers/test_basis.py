import os

from tests.fixtures.structural.references import CENTERED_BASIS_DATA
from tests.integration import IntegrationTestBase
from express.parsers.basis import BasisParser

class TestBasisParser(IntegrationTestBase):

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
            return BasisParser(**kwargs)

    def test_basis_centered_basis(self):
        self.centered_basis = self.parser.center_of_mass_basis()
        self.assertEqual(self.centered_basis, CENTERED_BASIS_DATA)
