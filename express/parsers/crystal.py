import pymatgen
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
        super().__init__(*args, **kwargs)

    def space_group_symbol(self):
        """
        Returns space group symbol.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.space_group_symbol
        """
        return {
            "value": pymatgen.symmetry.analyzer.SpacegroupAnalyzer(self.structure).get_space_group_symbol(),
            "tolerance": 0.3
        }

    def volume(self):
        """
        Returns volume.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.volume
        """
        return self.structure.volume

    def density(self):
        """
        Returns density.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.density
        """
        return self.structure.density
