import io
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
        if self.cell != "original" and self.cell != None: self.structure = STRUCTURE_MAP[self.cell](self.structure)

        # keep only one atom inside the basis in order to have the original lattice type
        self.lattice_only_structure = mg.Structure.from_str(self.structure_string, self.structure_format)  # deepcopy
        self.lattice_only_structure.remove_sites(range(1, len(self.structure.sites)))

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
