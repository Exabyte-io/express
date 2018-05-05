from express.properties import BaseProperty
from express.properties.scalar.p_norm import PNorm
from express.properties.scalar.volume import Volume
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
        self.derived_properties = []
        self.lattice_format = kwargs.get("lattice_format", "lattice_bravais")
        try:
            volume = Volume("volume", raw_data).serialize_and_validate()
            density = Density("density", raw_data).serialize_and_validate()
            symmetry = Symmetry("symmetry", raw_data).serialize_and_validate()
            self.derived_properties = [volume, density, symmetry]
            self.derived_properties.extend(self._elemental_ratios())
            self.derived_properties.extend(self._p_norms())
        except:
            pass

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
            "formula": self.raw_data.get("reduced_formula") or "",
            "unitCellFormula": self.raw_data.get("formula") or "",
            "lattice": self.raw_data.get(self.lattice_format),
            "basis": self.raw_data.get("basis"),
            "derivedProperties": self.derived_properties
        }

    def _elemental_ratios(self):
        """
        Returns a list of elemental ratios.

        Returns:
             list
        """
        elemental_ratios = []
        for element in self.raw_data["elemental_ratios"].keys():
            elemental_ratio = ElementalRatio("elemental_ratio", self.raw_data, element=element).serialize_and_validate()
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
            p_norms.append(PNorm("p-norm", self.raw_data, degree=degree).serialize_and_validate())
        return p_norms

    def serialize_and_validate(self):
        """
        Serialize the property and validate it against the schema.

        Returns:
            dict
        """
        instance = self._serialize()
        self.esse.validate(instance, self.esse.get_schema('material'))
        return instance
