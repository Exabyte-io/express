import io
import json

import pymatgen as mg
from pymatgen.core.structure import Structure
from ase.io import read, write
from jarvis.core.atoms import Atoms
from jarvis.io.vasp.inputs import Poscar

from express.parsers import BaseParser
from express.parsers.mixins.ionic import IonicDataMixin

STRUCTURE_MAP = {
    "primitive": lambda s: mg.symmetry.analyzer.SpacegroupAnalyzer(s).get_primitive_standard_structure(),
    "conventional": lambda s: mg.symmetry.analyzer.SpacegroupAnalyzer(s).get_conventional_standard_structure(),
}

PRECISION_MAP = {
    # decimal places
    "coordinates_crystal": 9,
    "coordinates_cartesian": 6,
    "angles": 4,
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
        super().__init__(*args, **kwargs)
        self.structure_string = kwargs.get("structure_string")
        self.structure_format = kwargs.get("structure_format")

        # convert espresso input into poscar
        if self.structure_format == "espresso-in":
            self.structure_format = "poscar"
            self.structure_string = self.espresso_input_to_poscar(self.structure_string)

        # convert jarvis-db-entry JSON into poscar
        if self.structure_format == "jarvis-db-entry":
            self.structure_format = "poscar"
            self.structure_string = self.jarvis_db_entry_json_to_poscar(self.structure_string)

        # cell_type is either original, primitive or conventional
        self.cell_type = kwargs.get("cell_type", "original")
        self.structure = Structure.from_str(self.structure_string, self.structure_format)
        if self.cell_type != "original":
            self.structure = STRUCTURE_MAP[self.cell_type](self.structure)

        # keep only one atom inside the basis in order to have the original lattice type
        self.lattice_only_structure = Structure.from_str(self.structure_string, self.structure_format)  # deepcopy
        self.lattice_only_structure.remove_sites(range(1, len(self.structure.sites)))

    def lattice_vectors(self):
        """
        Returns lattice vectors.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.lattice_vectors
        """
        precision = PRECISION_MAP["coordinates_cartesian"]
        return {
            "vectors": {
                "a": self._round(self.structure.lattice.matrix.tolist()[0], precision),
                "b": self._round(self.structure.lattice.matrix.tolist()[1], precision),
                "c": self._round(self.structure.lattice.matrix.tolist()[2], precision),
                "alat": 1.0,
            }
        }

    def lattice_bravais(self):
        """
        Returns lattice bravais.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.lattice_bravais
        """
        precision_coordinates = PRECISION_MAP["coordinates_cartesian"]
        precision_angles = PRECISION_MAP["angles"]
        return {
            "type": self._lattice_type(),
            "a": self._round(self.structure.lattice.a, precision_coordinates),
            "b": self._round(self.structure.lattice.b, precision_coordinates),
            "c": self._round(self.structure.lattice.c, precision_coordinates),
            "alpha": self._round(self.structure.lattice.alpha, precision_angles),
            "beta": self._round(self.structure.lattice.beta, precision_angles),
            "gamma": self._round(self.structure.lattice.gamma, precision_angles),
            "units": {"length": "angstrom", "angle": "degree"},
        }

    def _lattice_type(self):
        """
        Returns lattice type according to AFLOW (http://aflowlib.org/) classification.

        Returns:
             str
        """
        structure_ = self.lattice_only_structure if self.cell_type != "primitive" else self.structure
        try:
            # try getting the lattice type from the lattice only structure
            return self._lattice_type_from_structure(structure_)
        except Exception:
            try:
                # try getting the lattice type from the current structure
                return self._lattice_type_from_structure(self.structure)
            except Exception:
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
            "units": "crystal",
            "elements": [{"id": i, "value": v.species_string} for i, v in enumerate(self.structure.sites)],
            "coordinates": [
                {"id": i, "value": self._round(v.frac_coords.tolist(), PRECISION_MAP["coordinates_crystal"])}
                for i, v in enumerate(self.structure.sites)
            ],
        }

    def space_group_symbol(self):
        """
        Returns space group symbol.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.space_group_symbol
        """
        return {
            "value": mg.symmetry.analyzer.SpacegroupAnalyzer(self.structure).get_space_group_symbol(),
            "tolerance": 0.3,
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

    def elemental_ratios(self):
        """
        Returns elemental ratios.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.elemental_ratios
        """
        return {
            el.symbol: self.structure.composition.get_atomic_fraction(el) for el in self.structure.composition.elements
        }

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
        input_ = io.StringIO()
        input_.write(espresso_input)
        input_.seek(0)
        atoms = read(input_, format="espresso-in")
        output_ = io.StringIO()
        write(output_, atoms, format="vasp", vasp5=True)
        content = output_.getvalue()
        input_.close()
        output_.close()
        return content

    def jarvis_db_entry_json_to_poscar(self, jarvis_db_entry_json_str):
        """
        Extracts structure from jarvis atoms dictionary and returns in poscar format.

        Args:
            jarvis_atoms_json (dict): input content

        Returns:
            str: poscar
        """
        jarvis_db_entry = json.loads(jarvis_db_entry_json_str)
        atoms = Atoms.from_dict(jarvis_db_entry["atoms"])
        poscar = Poscar(atoms)
        content = poscar.to_string()
        return content
