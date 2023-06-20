import ase.io
import rdkit.Chem
from io import StringIO
from typing import Dict, Tuple

from express.parsers.structure import StructureParser
from express.parsers.settings import ASE_FORMATS


class MoleculeParser(StructureParser):
    """
    Molecule parser class.

    Args:
        structure_string (str): structure string.
        structure_format (str): structure format, poscar, cif or espresso-in.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ase_format = ASE_FORMATS[self.structure_format]
        self.inchi_long, self.inchi = self.get_inchi()

    def get_rdkit_mol(self) -> rdkit.Chem.Mol:
        """
        Function to create an RDKit molecule object from a structure string
        """
        ase_pdb = StringIO()

        material_file_string = StringIO(self.structure_string)
        ase_atoms = ase.io.read(material_file_string, format=self.ase_format)

        ase.io.write(ase_pdb, ase_atoms, format="proteindatabank")
        rdkit_mol_object = rdkit.Chem.rdmolfiles.MolFromPDBBlock(ase_pdb.getvalue())
        return rdkit_mol_object

    def get_inchi(self) -> Tuple[str, Dict[str, str]]:
        """
        Function calculates the International Chemical Identifier (InChI) string for a given structure.
        It returns the full InChI string that is calculated along with a shorter notation that omits
        the `InChI=` prefix and is stored as the 'inchi' value.

        Returns:
            Str, Dict

        Example:
            InChI=1S/H2O/h1H2,
            {
                "name": "inchi",
                "value": "1S/H2O/h1H2"
            }
        """

        rdkit_mol_object = self.get_rdkit_mol()

        if rdkit_mol_object is None:
            inchi_short = None
            inchi_long = None
        else:
            inchi_long = rdkit.Chem.inchi.MolToInchi(rdkit_mol_object)
            inchi_short = inchi_long.split("=")[1]
        inchi = {"name": "inchi", "value": inchi_short}
        return inchi_long, inchi

    def get_inchi_key(self) -> Dict[str, str]:
        """
        Function calculates the non-human readable InChI Hash value.

        Returns:
            Dict

        Example:
            InChI Key for H2O
            Dict: {
                      "name": "inchi_key",
                      "value": "XLYOFNOQVPJJNP-UHFFFAOYSA-N"
                  }
        """
        inchi_key_val: str = rdkit.Chem.inchi.InchiToInchiKey(self.inchi_long)
        inchi_key = {"name": "inchi_key", "value": inchi_key_val}
        return inchi_key
