from __future__ import absolute_import

import cStringIO
import pymatgen as mg
from ase.io import read, write

from express.parsers import BaseParser
from express.parsers.mixins.ionic import IonicDataMixin

STRUCTURE_MAP = {
    "primitive": lambda s: mg.symmetry.analyzer.SpacegroupAnalyzer(s).get_primitive_standard_structure(),
    "conventional": lambda s: mg.symmetry.analyzer.SpacegroupAnalyzer(s).get_conventional_standard_structure()
}


class StructureParser(BaseParser, IonicDataMixin):
    """
    Structure parser class.

    Args:
        args (list): args passed to the parser.
        kwargs (dict): kwargs passed to the parser.
            structure_string (str): structure string.
            structure_format (str): structure format, poscar or espresso-in.
    """

    def __init__(self, *args, **kwargs):
        super(StructureParser, self).__init__(*args, **kwargs)
        self.structure_string = kwargs.get("structure_string")
        self.structure_format = kwargs.get("structure_format")

        # convert espresso input into poscar
        if self.structure_format == "espresso-in":
            self.structure_format = "poscar"
            self.structure_string = self.espresso_input_to_poscar(self.structure_string)

        # cell is either original, primitive or conventional
        self.cell = kwargs["cell"]
        self.structure = mg.Structure.from_str(self.structure_string, self.structure_format)
        if self.cell != "original": self.structure = STRUCTURE_MAP[self.cell](self.structure)

        # keep only one atom inside the basis in order to have the original lattice type
        self.lattice_only_structure = mg.Structure.from_str(self.structure_string, self.structure_format)  # deepcopy
        self.lattice_only_structure.remove_sites(range(1, len(self.structure.sites)))

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

    def basis(self):
        """
        Returns basis.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.basis
        """
        return {
            'units': 'crystal',
            'elements': [{'id': i + 1, 'value': v.species_string} for i, v in enumerate(self.structure.sites)],
            'coordinates': [{'id': i + 1, 'value': v.frac_coords.tolist()} for i, v in enumerate(self.structure.sites)]
        }

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

    def formula(self):
        """
        Returns formula.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.formula
        """
        return self.structure.composition.formula

    def reduced_formula(self):
        """
        Returns reduced formula.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.reduced_formula
        """
        return self.structure.composition.reduced_formula

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

    def atomic_constraints(self):
        """
        Returns atomic constraints.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.atomic_constraints
        """
        return self.structure.site_properties.get("selective_dynamics")

    def espresso_input_to_poscar(self, espresso_input):
        """
        Extracts structure from espresso input file and returns in poscar format.

        Args:
            espresso_input (str): input file content

        Returns:
            str: poscar
        """
        input_ = cStringIO.StringIO()
        input_.write(espresso_input)
        input_.seek(0)
        atoms = read(input_, format="espresso-in")
        output_ = cStringIO.StringIO()
        write(output_, atoms, format="vasp", vasp5=True)
        content = output_.getvalue()
        input_.close()
        output_.close()
        return content
