from __future__ import absolute_import

import pymatgen as mg

from express.parsers import BaseParser
from express.parsers.mixins.ionic import IonicDataMixin

STRUCTURE_MAP = {
    "primitive": lambda s: mg.symmetry.analyzer.SpacegroupAnalyzer(s).get_primitive_standard_structure(),
    "conventional": lambda s: mg.symmetry.analyzer.SpacegroupAnalyzer(s).get_conventional_standard_structure()
}


class PyMatGenParser(BaseParser, IonicDataMixin):
    """
    Pymatgen parser class.
    """

    def __init__(self, *args, **kwargs):
        super(PyMatGenParser, self).__init__(*args, **kwargs)
        self.structure_string = kwargs.get("structure_string")
        self.structure_format = kwargs.get("structure_format")
        self.structure = mg.Structure.from_str(self.structure_string, self.structure_format)
        if kwargs.get("cell"):
            self.structure = STRUCTURE_MAP[kwargs.get("cell")](self.structure)

    def lattice_vectors(self):
        """
        Returns lattice vectors.

        Returns:
            dict

        Example:
            express.parsers.mixins.ionic.IonicDataMixin#lattice_vectors
        """
        return {
            'vectors': {
                'a': self.structure.lattice.matrix.tolist()[0],
                'b': self.structure.lattice.matrix.tolist()[1],
                'c': self.structure.lattice.matrix.tolist()[2],
                'alat': 1.0
            }
        }

    def lattice_bravais(self):
        """
        Returns lattice bravais.

        Returns:
            dict

        Example:
            express.parsers.mixins.ionic.IonicDataMixin#lattice_bravais
        """
        return {
            "type": self._lattice_type(),
            "a": self.structure.lattice.a,
            "b": self.structure.lattice.b,
            "c": self.structure.lattice.c,
            "alpha": self.structure.lattice.alpha,
            "beta": self.structure.lattice.beta,
            "gamma": self.structure.lattice.gamma,
            "units": {
                "length": "angstrom",
                "angle": "degree"
            }
        }

    def _lattice_type(self):
        """
        Returns lattice type according to AFLOW (http://aflowlib.org/) classification.

        Returns:
             str
        """
        analyzer = mg.symmetry.analyzer.SpacegroupAnalyzer(self.structure, symprec=0.001)
        lattice_type = analyzer.get_lattice_type()
        spg_symbol = analyzer.get_spacegroup_symbol()

        # TODO: find a better implementation
        if lattice_type == "cubic":
            if "P" in spg_symbol:
                return "CUB"
            elif "F" in spg_symbol:
                return "FCC"
            elif "I" in spg_symbol:
                return "BCC"
        elif lattice_type == "tetragonal":
            if "P" in spg_symbol:
                return "TET"
            elif "I" in spg_symbol:
                return "BCT"
        elif lattice_type == "orthorhombic":
            if "P" in spg_symbol:
                return "ORC"
            elif "F" in spg_symbol:
                return "ORCF"
            elif "I" in spg_symbol:
                return "ORCI"
            elif "C" in spg_symbol:
                return "ORCC"
        elif lattice_type == "hexagonal":
            return "HEX"
        elif lattice_type == "rhombohedral":
            return "RHL"
        elif lattice_type == "monoclinic":
            if "P" in spg_symbol:
                return "MCL"
            elif "C" in spg_symbol:
                return "MCLC"

        return "TRI"

    def basis(self):
        """
        Returns basis.

        Returns:
            dict

        Example:
            express.parsers.mixins.ionic.IonicDataMixin#basis
        """
        return {
            'units': 'crystal',
            'elements': [{'id': i + 1, 'value': v.species_string} for i, v in enumerate(self.structure.sites)],
            'coordinates': [{'id': i + 1, 'value': v.frac_coords.tolist()} for i, v in enumerate(self.structure.sites)]
        }

    def space_group_symbol(self):
        """
        Returns space group symbol.

        Returns:
             str
        """
        return {
            "value": mg.symmetry.analyzer.SpacegroupAnalyzer(self.structure).get_spacegroup_symbol(),
            "tolerance": 0.3
        }

    def formula(self):
        """
        Returns formula.

        Return:
             str
        """
        return self.structure.composition.formula

    def reduced_formula(self):
        """
        Returns reduced formula.

        Return:
             str
        """
        return self.structure.composition.reduced_formula

    def volume(self):
        """
        Returns volume.

        Returns:
             float
        """
        return self.structure.volume

    def elemental_ratios(self):
        """
        Returns elemental ratios.

        Returns:
            dict
        """
        return {
            el.symbol: self.structure.composition.get_atomic_fraction(el) for el in self.structure.composition.elements
        }

    def density(self):
        """
        Returns density.

        Returns:
             float
        """
        return self.structure.density
