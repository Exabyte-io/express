from express.properties import BaseProperty
from express.properties.scalar.p_norm import PNorm
from express.properties.scalar.volume import Volume
from express.parsers.pymatgen import PyMatGenParser
from express.properties.scalar.density import Density
from express.properties.non_scalar.symmetry import Symmetry
from express.properties.scalar.elemental_ratio import ElementalRatio


class Material(BaseProperty):
    """
    Material class.

    Args:
        raw_data (dict): raw data used to form the material.
        cell (str): either primitive or conventional.
        args (list): material-specific args.
        kwargs (dict): material-specific kwargs.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        super(Material, self).__init__(name, raw_data, *args, **kwargs)

        cell = kwargs.get("cell", "original")
        structure_string = kwargs.get("structure_string")
        structure_format = kwargs.get("structure_format", "poscar")

        if not structure_string:
            is_initial_structure = kwargs.get("is_initial_structure")
            if is_initial_structure:
                basis = self.raw_data.get("initial_basis")
                lattice = self.raw_data.get("initial_lattice_vectors")
                structure_string = self._to_poscar(lattice, basis)

            is_final_structure = kwargs.get("is_final_structure")
            if is_final_structure:
                basis = self.raw_data.get("final_basis")
                lattice = self.raw_data.get("final_lattice_vectors")
                structure_string = self._to_poscar(lattice, basis)

        self.pymatgen = PyMatGenParser(structure_string=structure_string, structure_format=structure_format, cell=cell)

    @property
    def formula(self):
        return self.pymatgen.reduced_formula()

    @property
    def unitCellFormula(self):
        return self.pymatgen.formula()

    @property
    def derived_properties(self):
        derived_properties = []
        try:
            raw_data = {
                "volume": self.pymatgen.volume(),
                "density": self.pymatgen.density(),
                "elemental_ratios": self.pymatgen.elemental_ratios(),
                "space_group_symbol": self.pymatgen.space_group_symbol(),
            }
            volume = Volume("volume", raw_data).serialize_and_validate()
            density = Density("density", raw_data).serialize_and_validate()
            symmetry = Symmetry("symmetry", raw_data).serialize_and_validate()
            derived_properties = [volume, density, symmetry]
            derived_properties.extend(self._elemental_ratios(raw_data))
            derived_properties.extend(self._p_norms(raw_data))
        except:
            pass
        return derived_properties

    @property
    def basis(self):
        return self.pymatgen.basis()

    @property
    def lattice(self):
        return self.pymatgen.lattice_bravais()

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

    def _elemental_ratios(self, raw_data):
        """
        Returns a list of elemental ratios.

        Returns:
             list
        """
        elemental_ratios = []
        for element in raw_data["elemental_ratios"].keys():
            elemental_ratio = ElementalRatio("elemental_ratio", raw_data, element=element).serialize_and_validate()
            elemental_ratios.append(elemental_ratio)
        return elemental_ratios

    def _p_norms(self, raw_data):
        """
        Returns a list of p-norms.

        Reference:
            https://images.nature.com/full/nature-assets/npjcompumats/2016/npjcompumats201628/extref/npjcompumats201628-s1.pdf

        Returns:
            list
        """
        p_norms = []
        for degree in [0, 2, 3, 5, 7, 10]:
            p_norms.append(PNorm("p-norm", raw_data, degree=degree).serialize_and_validate())
        return p_norms

    def _get_unique_elements(self, basis):
        return list(set([e["value"] for e in basis["elements"]]))

    def _get_element_count(self, el, basis):
        return len([x for x in basis["elements"] if x["value"] == el])

    def _to_poscar(self, lattice, basis):
        return "\n".join([
            "material",
            "1.0",
            "\t".join(["{0:14.9f}".format(x) for x in lattice["vectors"]["a"]]),
            "\t".join(["{0:14.9f}".format(x) for x in lattice["vectors"]["b"]]),
            "\t".join(["{0:14.9f}".format(x) for x in lattice["vectors"]["c"]]),
            " ".join(self._get_unique_elements(basis)),
            " ".join([str(self._get_element_count(el, basis)) for el in self._get_unique_elements(basis)]),
            "cartesian",
            "\n".join([" ".join(["{0:14.9f}".format(v) for v in x["value"]]) for x in basis["coordinates"]])
        ])
