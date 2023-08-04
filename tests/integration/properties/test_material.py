import os
from copy import deepcopy
from typing import Dict, List

from express.parsers.apps.espresso.parser import EspressoParser
from express.parsers.apps.vasp.parser import VaspParser
from express.properties.material import Material
from tests.fixtures.data import SI as data
from tests.integration import IntegrationTestBase


class MaterialTest(IntegrationTestBase):
    def setUp(self):
        super(MaterialTest, self).setUp()

    def tearDown(self):
        super(MaterialTest, self).tearDown()

    @property
    def vasp_parser(self):
        return VaspParser(work_dir=self.workDir, stdout_file=self.stdoutFile)

    @property
    def espresso_parser(self):
        return EspressoParser(work_dir=self.workDir, stdout_file=self.stdoutFile)

    @property
    def structure_string(self):
        manifest = self.getManifest()
        with open(os.path.join(self.rootDir, manifest["structurePath"])) as f:
            return f.read()

    def assertPropertiesEqual(self, material: Material) -> bool:
        """Assert all Si properties match expected values."""
        self.assertDeepAlmostEqual(material.formula, data["formula"], places=2)
        self.assertDeepAlmostEqual(material.unitCellFormula, data["unitCellFormula"], places=2)
        self.assertDeepAlmostEqual(material.basis, data["basis"], places=2)
        self.assertDeepAlmostEqual(material.lattice, data["lattice"], places=2)
        # derived properties is a list of dicts, sort by name so assertDeepAlmostEqual works
        derived_props = self.filter_derived_props(material.is_non_periodic)
        self.assertDeepAlmostEqual(material.derived_properties, derived_props, places=2)
        return True

    def assertJsonEqual(self, material: Material) -> bool:
        """Assert serialzed material matches expected JSON."""
        derived_props = self.filter_derived_props(material.is_non_periodic)
        json = deepcopy(data)
        json["derivedProperties"] = derived_props
        self.assertDeepAlmostEqual(material.serialize_and_validate(), json, places=2)
        return True

    def filter_derived_props(self, is_non_periodic: bool = False) -> List[Dict]:
        derived_props = sorted(data["derivedProperties"], key=lambda x: x["name"])
        if is_non_periodic:
            # remove volume and density from fixtures since they are not calculated if non-periodic
            filtered_derived_props = [prop for prop in derived_props if prop["name"] not in ["volume", "density"]]
        else:
            # remove inchi keys from fixture since they are not calculated if periodic
            filtered_derived_props = [prop for prop in derived_props if not prop["name"].startswith("inchi")]
        return filtered_derived_props

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

    def test_material_is_non_periodic(self):
        material = Material("material", self.vasp_parser, is_initial_structure=True, is_non_periodic=True)
        self.assertPropertiesEqual(material)

    def test_material_from_structure(self):
        material = Material(
            "material",
            parser=None,
            cell_type="original",
            structure_string=self.structure_string,
            structure_format="espresso-in",
            is_non_periodic=True,
        )
        self.assertPropertiesEqual(material)

    def test_material_serialize_and_validate(self):
        material = Material("material", self.vasp_parser, is_initial_structure=True, is_non_periodic=True)
        self.assertJsonEqual(material)
