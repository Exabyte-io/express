import ase.io
import rdkit.Chem
from io import StringIO
from typing import Dict, Tuple
import pymatgen
from express.parsers.structure import StructureParser
from express.parsers.utils import convert_to_ase_format


class MoleculeParser(StructureParser):
    """
    Molecule parser class.

    Args:
        structure_string (str): structure string.
        structure_format (str): structure format, poscar, cif or espresso-in.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ase_format = convert_to_ase_format(self.structure_format)
        self.inchi_long, self.inchi = self.get_inchi()
        self.pymatgen_molecule = pymatgen.core.structure.Molecule.from_str(self.get_xyz_string(), 'xyz')

    def n_atoms(self):
        """
        Returns number of atoms in a molecule

        Returns: Number
        """
        return len(self.pymatgen_molecule.sites)

    def point_group_symbol(self):
        """
        Returns point group symbol.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.point_group_symbol
        """

        point_group_symbol = str(pymatgen.symmetry.analyzer.PointGroupAnalyzer(self.pymatgen_molecule).get_pointgroup())
        point_group = {
            "value": point_group_symbol,
            "tolerance": 0.3
        }
        return point_group

    def get_rdkit_molecule(self) -> rdkit.Chem.Mol:
        """
        Function to create an RDKit molecule object from a structure string
        """
        ase_pdb = StringIO()

        molecule_file_string = StringIO(self.structure_string)
        ase_atoms = ase.io.read(molecule_file_string, format=self.ase_format)

        ase.io.write(ase_pdb, ase_atoms, format="proteindatabank")
        rdkit_molecule_object = rdkit.Chem.rdmolfiles.MolFromPDBBlock(ase_pdb.getvalue())
        return rdkit_molecule_object

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

        rdkit_molecule_object = self.get_rdkit_molecule()

        if rdkit_molecule_object is None:
            inchi_short = None
            inchi_long = None
        else:
            inchi_long = rdkit.Chem.inchi.MolToInchi(rdkit_molecule_object)
            inchi_short = inchi_long.split("=")[1]
        inchi = {
            "name": "inchi",
            "value": inchi_short
        }
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
        inchi_key = {
            "name": "inchi_key",
            "value": inchi_key_val
        }
        return inchi_key

    def get_xyz_string(self):
        """
        Function returns an xyz string of a structure
        """
        molecule_file_string = StringIO(self.structure_string)
        ase_atoms = ase.io.read(molecule_file_string, format=self.ase_format)
        xyz = StringIO()
        ase.io.write(xyz, ase_atoms, format='xyz')
        return xyz.getvalue()
