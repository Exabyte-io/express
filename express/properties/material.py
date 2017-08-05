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
        self.volume = Volume("volume", raw_data).serialize_and_validate()
        self.density = Density("density", raw_data).serialize_and_validate()
        self.symmetry = Symmetry("symmetry", raw_data).serialize_and_validate()
        self.derived_properties = [self.volume, self.density, self.symmetry]
        self.derived_properties.extend(self._elemental_ratios())
        self.derived_properties.extend(self._p_norms())

    def _serialize(self):
        """
        Serialize a material.

        Returns:
             dict
        """
        return {
            "name": "",
            "_id": "",
            "exabyteId": "",
            "formula": self.raw_data["reduced_formula"],
            "unitCellFormula": self.raw_data["formula"],
            "lattice": self.raw_data["lattice_bravais"],
            "basis": self.raw_data["basis"],
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
