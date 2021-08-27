from io import StringIO

import os
import ase
from ase.io import read
from ase.io import write
import rdkit
from rdkit import Chem
import logging
import tempfile

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
        self.inchi_long, self.inchi = self.get_inchi()

    def create_pdb_from_poscar(self):
        """
        Function to create pdb mol string object from a poscar string
        """
        pdb_string = StringIO()
        ase_pdb = StringIO()
        pdb = tempfile.TemporaryFile()
        poscar_string = StringIO(self.structure_string)
        ase_poscar = ase.io.read(poscar_string, format="vasp")
        ase.io.write(ase_pdb, ase_poscar, format="proteindatabank")
        pdbmol = rdkit.Chem.rdmolfiles.MolFromPDBBlock(ase_pdb.getvalue())
        return pdbmol

    def get_inchi(self):
        """
        Function calculates the International Chemical Identifier (InChI) string for a given structure.

        Returns:
            Str: structure in InChI format.
        """

        pdbmol = self.create_pdb_from_poscar()
        inchi_long = rdkit.Chem.inchi.MolToInchi(pdbmol)
        inchi_short = inchi_long.split("=")
        inchi = inchi_short[1]
        inchi_str = {
            "name": "inchi",
            "value": inchi
        }
        return inchi_long, inchi_str

    def get_inchi_key(self):
        """
        Function calculates the non-human readable InChI Hash value.

        Returns:
            Str: Structure in InChI Key format.
        """
        inchi_key_val = rdkit.Chem.inchi.InchiToInchiKey(self.inchi_long)
        inchi_key_str = {
            "name": "inchi_key",
            "value": inchi_key_val
        }
        return inchi_key_str
