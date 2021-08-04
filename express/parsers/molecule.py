from io import StringIO
import os
from ase.io import read, write
import ase
import rdkit
from rdkit import Chem
import logging

class MoleculeParser():
    """
    Molecule parser class.

    Args:
        args (list): args passed to the parser.
        kwargs (dict): kwargs passed to the parser.
            structure_string (str): structure string.
            structure_format (str): structure format, poscar or espresso-in.
    """

    def __init__(self, structure_string):
        self.structure_string = structure_string
        self.is_using_inchi = self.is_pybel_import_successful()


    def is_pybel_import_successful(self):
        """
        pybel is a submodule of openbabel used to generate the molecule string that
        can then be converted into an InChI string by rdkit.

        Pybel can be imported when the butler-venv is running.
        Without the butler-venv, openbabel is not installed, thereby causing
        the pybel import to fail.

        When the butler-venv is not installed, inchi generation will be
        set to 'None' and essentially skipped for the purpose of testing.

        Without the 'try' statements present below ExPrESS will fail due to import errors.
        If openbabel is installed properly pybel will be imported.
        Otherwise, pybel import will fail and then get_inchi & get_inchi_key will
        be set to 'None'

        Returns:
            Int:
                0 = import failed, do not run InChI generation.
                1 = import successful, run InChI generation.
        """
        try:
            import pybel
            is_using_inchi = 1
        except ImportError:
            is_using_inchi = 0
            logging.error("Pybel failed to import. InChI & InChI Key cannot be created.")
        return is_using_inchi

    def create_pybel_smile_from_poscar(self):
        """
        Function using ase to convert the POSCAR formatted string of a structure
        into an XYZ formatted text file for that structure.

        Then pybel converts the XYZ formatted text file into a SMILES format.

        Returns:
            Str: structure in SMILES format.
        """
        import pybel
        xyz_file = "geom.xyz"
        with open(xyz_file, "w") as file:
            os.chmod(xyz_file, 0o777)
            file_string = StringIO(self.structure_string)
            ase_poscar = ase.io.read(file_string, format="vasp")
            ase_xyz_file = ase.io.write(xyz_file, ase_poscar, format='xyz')
            pybel_smile = list(pybel.readfile('xyz', 'geom.xyz'))[0]
        return pybel_smile

    def get_inchi(self):
        """
        Function calculates the International Chemical Identifier (InChI) string for a given structure.

        Returns:
            Str: structure in InChI format.
        """
        if self.is_using_inchi == 0:
            inchi_short = ''
        else:
            pybel_smile = self.create_pybel_smile_from_poscar()
            self.inchi = pybel_smile.write("inchi")
            inchi_short = self.inchi.split("=")
            inchi_short = inchi_short[1]

        inchi_str = {
            "name": "inchi",
            "value": inchi_short
        }
        return inchi_str

    def get_inchi_key(self):
        """
        Function calculates the non-human readable InChI Hash value.

        Returns:
            Str: Structure in InChI Key format.
        """
        if self.is_using_inchi == 0:
            inchi_key_val = ''
        else:
            inchi_key_val = Chem.inchi.InchiToInchiKey(self.inchi)

        inchi_key_str = {
            "name": "inchi_key",
            "value": inchi_key_val
        }
        return inchi_key_str
