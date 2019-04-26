import os

from express.properties import BaseProperty
from express.properties.scalar.p_norm import PNorm
from express.properties.scalar.volume import Volume
from express.parsers.structure import StructureParser
from express.properties.scalar.density import Density
from express.parsers.apps.vasp.parser import VaspParser
from express.properties.non_scalar.symmetry import Symmetry
from express.properties.scalar.elemental_ratio import ElementalRatio


class Material(BaseProperty):
    """
    Material class.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(Material, self).__init__(name, parser, *args, **kwargs)

        cell = kwargs.get("cell", "original")
        structure_string = kwargs.get("structure_string")
        structure_format = kwargs.get("structure_format", "poscar")

        if not structure_string:
            if kwargs.get("is_initial_structure"):
                if isinstance(self.parser, VaspParser):
                    with open(os.path.join(self.parser.work_dir, "POSCAR")) as f:
                        structure_string = f.read()
                else:
                    basis = self.parser.initial_basis()
                    lattice = self.parser.initial_lattice_vectors()
                    structure_string = self._to_poscar(lattice, basis)

            if kwargs.get("is_final_structure"):
                if isinstance(self.parser, VaspParser):
                    with open(os.path.join(self.parser.work_dir, "CONTCAR")) as f:
                        structure_string = f.read()
                else:
                    basis = self.parser.final_basis()
                    lattice = self.parser.final_lattice_vectors()
                    structure_string = self._to_poscar(lattice, basis)

        # override parser to use StructureParser from now on
        self.parser = StructureParser(structure_string=structure_string, structure_format=structure_format, cell=cell)

    @property
    def formula(self):
        return self.parser.reduced_formula()

    @property
    def unitCellFormula(self):
        return self.parser.formula()

    @property
    def derived_properties(self):
        derived_properties = []
        try:
            volume = Volume("volume", self.parser).serialize_and_validate()
            density = Density("density", self.parser).serialize_and_validate()
            symmetry = Symmetry("symmetry", self.parser).serialize_and_validate()
            derived_properties = [volume, density, symmetry]
            derived_properties.extend(self._elemental_ratios())
            derived_properties.extend(self._p_norms())
        except:
            pass
        return derived_properties

    @property
    def basis(self):
        return self.parser.basis()

    @property
    def lattice(self):
        return self.parser.lattice_bravais()

    def _serialize(self):
        """
        Serialize a material.

        Returns:
             dict
        """
        return {
            "_id": "",
            "name": self.name,
            "exabyteId": "",
            "hash": "",
            "formula": self.formula,
            "unitCellFormula": self.unitCellFormula,
            "lattice": self.lattice,
            "basis": self.basis,
            "derivedProperties": self.derived_properties,
            "creator": {
                "_id": "",
                "cls": "User",
                "slug": ""
            },
            "owner": {
                "_id": "",
                "cls": "Account",
                "slug": ""
            },
            "schemaVersion": "0.2.0",
        }

    def _elemental_ratios(self):
        """
        Returns a list of elemental ratios.

        Returns:
             list
        """
        elemental_ratios = []
        for element in self.parser.elemental_ratios().keys():
            elemental_ratio = ElementalRatio("elemental_ratio", self.parser, element=element).serialize_and_validate()
            elemental_ratios.append(elemental_ratio)
        return elemental_ratios

    def _p_norms(self):
        """
        Returns a list of p-norms.

        Reference:
            https://images.nature.com/full/nature-assets/npjcompumats/2016/npjcompumats201628/extref/npjcompumats201628-s1.pdf

        Returns:
            list
        """
        p_norms = []
        for degree in [0, 2, 3, 5, 7, 10]:
            p_norms.append(PNorm("p-norm", self.parser, degree=degree).serialize_and_validate())
        return p_norms

    def _get_element_counts(self, basis):
        """
        Returns chemical elements with their count wrt their original order in the basis.
        Note: entries for the same element separated by another element are considered separately.
        [{"count":1, "value":"Zr"}, {"count":23, "value":"H"}, {"count":11, "value":"Zr"}, {"count":1, "value":"H"}]
        """
        element_counts = []
        previous_element = None
        for index, element in enumerate(basis["elements"]):
            if previous_element and previous_element["value"] == element["value"]:
                element_counts[-1]["count"] += 1
            else:
                element_counts.append({
                    "count": 1,
                    "value": element["value"]
                })
            previous_element = basis["elements"][index]
        return element_counts

    def _to_poscar(self, lattice, basis):
        element_counts = self._get_element_counts(basis)
        return "\n".join([
            "material",
            "1.0",
            "\t".join(["{0:14.9f}".format(x) for x in lattice["vectors"]["a"]]),
            "\t".join(["{0:14.9f}".format(x) for x in lattice["vectors"]["b"]]),
            "\t".join(["{0:14.9f}".format(x) for x in lattice["vectors"]["c"]]),
            " ".join((e["value"] for e in element_counts)),
            " ".join((str(e["count"]) for e in element_counts)),
            "cartesian",
            "\n".join([" ".join(["{0:14.9f}".format(v) for v in x["value"]]) for x in basis["coordinates"]])
        ])
