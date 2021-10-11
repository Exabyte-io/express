import io
import pymatgen as mg
from ase.io import read, write

from express.parsers.structure import StructureParser


class CrystalParser(StructureParser):
    """
    Crystal  parser class.

    Args:
        args (list): args passed to the parser.
        kwargs (dict): kwargs passed to the parser.
            structure_string (str): structure string.
            structure_format (str): structure format, poscar or espresso-in.
    """

    def __init__(self, *args, **kwargs):
        super(CrystalParser, self).__init__(*args, **kwargs)

    def lattice_vectors(self):
        """
        Returns lattice vectors.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.lattice_vectors
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

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.lattice_bravais
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
        structure_ = self.lattice_only_structure if self.cell != "primitive" else self.structure
        try:
            # try getting the lattice type from the lattice only structure
            return self._lattice_type_from_structure(structure_)
        except:
            try:
                # try getting the lattice type from the current structure
                return self._lattice_type_from_structure(self.structure)
            except:
                return "TRI"

    def _lattice_type_from_structure(self, structure_):
        """
        Returns lattice type according to AFLOW (http://aflowlib.org/) classification.

        Returns:
             str
        """
        analyzer = mg.symmetry.analyzer.SpacegroupAnalyzer(structure_, symprec=0.001)
        lattice_type = analyzer.get_lattice_type()
        spg_symbol = analyzer.get_space_group_symbol()

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

    def volume(self):
        """
        Returns volume.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.volume
        """
        return self.structure.volume

    def elemental_ratios(self):
        """
        Returns elemental ratios.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.elemental_ratios
        """
        return {
            el.symbol: self.structure.composition.get_atomic_fraction(el) for el in self.structure.composition.elements
        }

    def density(self):
        """
        Returns density.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.density
        """
        return self.structure.density

    def space_group_symbol(self):
        """
        Returns space group symbol.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.space_group_symbol
        """
        return {
            "value": mg.symmetry.analyzer.SpacegroupAnalyzer(self.structure).get_space_group_symbol(),
            "tolerance": 0.3
        }
