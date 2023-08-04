from express.parsers.apps.espresso.parser import EspressoParser
from express.parsers.apps.vasp.parser import VaspParser
from express.properties.material import Material
from tests.fixtures.data import SI
from tests.integration import IntegrationTestBase


class MaterialTest(IntegrationTestBase):
    def setUp(self):
        super(MaterialTest, self).setUp()

    def tearDown(self):
        super(MaterialTest, self).setUp()

    @property
    def vasp_parser(self):
        return VaspParser(work_dir=self.workDir, stdout_file=self.stdoutFile)

    @property
    def espresso_parser(self):
        return EspressoParser(work_dir=self.workDir, stdout_file=self.stdoutFile)

    def assertPropertiesEqual(self, material: Material) -> bool:
        """Assert all Si properties match expected values."""
        return (
            self.assertDeepAlmostEqual(material.formula, SI["formula"])
            and self.assertDeepAlmostEqual(material.unitCellFormula, SI["unitCellFormula"])
            and self.assertDeepAlmostEqual(material.basis, SI["basis"], places=2)
            and self.assertDeepAlmostEqual(material.lattice, SI["lattice"], places=2)
            and self.assertDeepAlmostEqual(material.derived_properties, SI["derived_properties"])
        )

    """
    constructor
        if not structure string, build structure string in VASP format based on application
            is intial structure:
                vasp -> read poscar
                espresso -> initial_basis + initial_lattice_vectors = poscar
            else is final structure:
                vasp -> read contcar
                espresso -> final_basis + final_lattice_vectors = POSCAR

        if non-periodic:
            parse using MoleculeParser

        else:
            parse using CrystalParser

    test properties match expected output
        formula
        unitCellFormula
        basis
        lattice
        derived_properties

    test serialize_and_validate
    """

    def test_material_vasp_initial_structure(self):
        material = Material("material", self.vasp_parser, is_initial_structure=True)
        self.assertPropertiesEqual(material)

    def test_material_vasp_final_structure(self):
        material = Material("material", self.vasp_parser, is_final_structure=True)
        self.assertPropertiesEqual(material)

    def test_material_espresso_initial_structure(self):
        material = Material("material", self.espresso_parser, is_initial_structure=True)
        self.assertPropertiesEqual(material)

    def test_material_espresso_final_structure(self):
        material = Material("material", self.espresso_parser, is_final_structure=True)
        self.assertPropertiesEqual(material)

    def test_material_periodic_structure(self):
        pass

    def test_material_nonperiodic_structure(self):
        pass
