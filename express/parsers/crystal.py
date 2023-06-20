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
