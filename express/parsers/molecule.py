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
        structure_string (str): structure string.
        structure_format (str): structure format, poscar or espresso-in.
    """

    def __init__(self, structure_string: str, structure_format: str):
        self.structure_string = structure_string

        if structure_format == "poscar":
            self.ase_format = "vasp"
        else:
            self.ase_format = structure_format

        self.inchi_long, self.inchi = self.get_inchi()

    def create_rdkit_molfrom_structure(self):
        """
        Function to create an RDKit molecule object from a structure string
        """
        ase_pdb = StringIO()

        material_file_string = StringIO(self.structure_string)
        ase_atoms = ase.io.read(material_file_string, format=self.ase_format)

        ase.io.write(ase_pdb, ase_atoms, format="proteindatabank")
        pdbmol = rdkit.Chem.rdmolfiles.MolFromPDBBlock(ase_pdb.getvalue())
        return pdbmol

    def get_inchi(self):
        """
        Function calculates the International Chemical Identifier (InChI) string for a given structure.

        Returns:
            Str: structure in InChI format.
        """

        pdbmol = self.create_rdkit_molfrom_structure()
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
