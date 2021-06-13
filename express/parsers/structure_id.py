import io
import pymatgen as mg
from pymatgen.io.xyz import XYZ
from ase.io import read, write
import rdkit
from express.parsers import BaseParser
from express.parsers.mixins.ionic import IonicDataMixin

"""
    openbabel & pybel work together to generate the molecule string that
    can then be converted into an InChI string by rdkit.

    openbabel & pybel can be imported when the butler-venv is running.
    Without the butler-venv, openbabel is not installed and therefore
    both imports will fail.

    When the butler-venv is not installed, inchi generation will be 
    set to 'None' and essentially skipped for the purpose of testing.

    Without the 'try' statements ExPrESS will fail due to import errors.

    If the openbabel import is successul, then pybel will be imported.
    If the openbabel import fails, then get_inchi & get_inchi_key will
    be set to 'None'
"""
try:
    import openbabel
    import pybel
    inchi_run  = 1
except ImportError:
    print("WARNING: openbabel & pybel import failed. Inchi's will be turned off!")
    inchi_run = 0

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
        if inchi_run == 0:
            print("inchi run: {}".format(inchi_run))
            return ''
        else:
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
        if inchi_run == 0:
            print("inchi run: {}".format(inchi_run))
            return ''
        else:
            inchi = self.inchi
            self.inchi_key = rdkit.Chem.inchi.InchiToInchiKey(inchi)
            return self.inchi_key
