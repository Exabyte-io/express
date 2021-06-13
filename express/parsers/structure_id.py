import io
import pymatgen as mg
from pymatgen.io.xyz import XYZ
from ase.io import read, write
import rdkit
import openbabel
import pybel
from express.parsers import BaseParser
from express.parsers.mixins.ionic import IonicDataMixin


class Identifier(BaseParser, IonicDataMixin):

    def __init__(self, *args, **kwargs):
        super(Identifier, self).__init__(*args, **kwargs)
        self.structure_string = kwargs.get("structure_string")
        self.structure_format = kwargs.get("structure_format")

        # convert espresso input into poscar
        if self.structure_format == "espresso-in":
            self.structure_format = "poscar"
            self.structure_string = self.espresso_input_to_poscar(self.structure_string)

    def get_inchi(self):
        """
        Function calculates the International Chemical Identifier (InChI) string for a given structure.

        Returns:
            Str
        """
        cart = XYZ.from_string(self.structure_string)
        cart.write_file("geom.xyz")
        xyz_file = "geom.xyz"
        inchi_read = list(pybel.readfile('xyz', xyz_file))[0]
        self.inchi = inchi_read.write("inchi")
        inchi_hash = inchi.split("=")
        self.inchi_hash = inchi_hash[1]
        return self.inchi_hash


    def get_inchi_key(self):
        """
        Function converts a human readable InChI into a computer readable Hash string.

        Returns:
            Str
        """
        inchi = self.inchi
        self.inchi_key = rdkit.Chem.inchi.InchiToInchiKey(inchi)
        return self.inchi_key
