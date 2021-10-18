import ase.io
import rdkit.Chem
from io import StringIO
from typing import Dict, Tuple
import pymatgen as mg
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
        self.mg_mol = mg.core.structure.Molecule.from_str(self.get_pymatgen_mol(), 'xyz')

    def n_atoms(self):
        """
        Function that returns the number of atoms in a molecule.

        Returns:
            Int
        """
        return len(self.mg_mol)

    def point_group_symbol(self):
        """
        Returns point group symbol.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.point_group_symbol
        """

        point_group_symbol = str(mg.symmetry.analyzer.PointGroupAnalyzer(self.mg_mol).get_pointgroup())
        point_group = {
            "name": "symmetry",
            "pointGroupSymbol": point_group_symbol,
            "tolerance": {
                "units": "angstrom",
                "value": 0.3
            }
        }
        return point_group

    def get_rdkit_mol(self) -> rdkit.Chem.Mol:
        """
        Function to create an RDKit molecule object from a structure string
        """
        ase_pdb = StringIO()

        molecule_file_string = StringIO(self.structure_string)
        ase_atoms = ase.io.read(molecule_file_string, format=self.ase_format)

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

    def get_pymatgen_mol(self):
        """
        Function returns a pymatgen molecule object
        """
        molecule_file_string = StringIO(self.structure_string)
        ase_atoms = ase.io.read(molecule_file_string, format=self.ase_format)
        ase_xyz = StringIO()
        ase.io.write(ase_xyz, ase_atoms, format='xyz')
        return ase_xyz.getvalue()

    def get_center_of_mass_molecule(self):
        """
        Function returns XYZ coordinates for a molecule centered around its center of mass.
        """
        return self.mg_mol.get_centered_molecule()

    def find_max_radii(self):
        """
        Function returns the atoms with the max radii and the max radii of a molecule
        """
        radii = {}
        atom_counter_a = 0
        atom_counter_b = 1
        total_atoms = self.n_atoms()
        while atom_counter_a < total_atoms:
            while atom_counter_b < total_atoms:
                atom_pair = str(atom_counter_a) + '_' + str(atom_counter_b)
                dist = self.mg_mol.get_distance(atom_counter_a, atom_counter_b)
                radii[atom_pair] = dist
                atom_counter_b += 1
            atom_counter_a += 1
            atom_counter_b = atom_counter_a + 1

        max_distance = max(radii.values())
        for key in radii.keys():
            if radii[key] == max_distance:
                max_distance_atom_pair = key.split('_')

        max_radii = {
            "name": "max-molecule-radii",
            "atom-pair": [
                {
                    "id": int(max_distance_atom_pair[0]),
                },
                {
                    "id": int(max_distance_atom_pair[1])
                }
            ],
            "distance":{
                "value": max_distance,
                "units": "angstrom"
            }
        }
        return max_radii
