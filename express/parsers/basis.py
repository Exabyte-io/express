from express.parsers.molecule import MoleculeParser
import pymatgen


class BasisParser(MoleculeParser):
    """
    Molecule parser class.

    Args:
        structure_string (str): structure string.
        structure_format (str): structure format, poscar, cif or espresso-in.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def center_of_mass_basis(self):
        """
        Function returns the XYZ basis for a molecule centered around the center of mass of the molecule.

        Example:
            "elements": [
                {
                    "id": 1,
                    "value": "O"
                },
                {
                    "id": 2,
                    "value": "O"
                }
           ],
           "name": "atomic_coordinates",
           "values": [
               {
                   "id": 1,
                   "value": [
                       -0.60400,
                       0.00000,
                       0.00000
                   ]
               },
               {
                   "id": 2,
                   "value": [
                       0.60400,
                       0.00000,
                       0.00000
                   ]
               }
           ]
        """
        centered_molecule = self.pymatgen_molecule.get_centered_molecule()
        centered_molecule_dict = centered_molecule.as_dict()
        centered_molecule_basis = centered_molecule_dict['sites']

        centered_basis = {}
        basis_elements = []
        basis_coordinates = []
        for i, element in enumerate(centered_molecule_basis):
            atom_dict = {}
            coord_dict = {}
            element_array = []

            atom_dict["id"] = coord_dict["id"] = i + 1
            atom_dict["value"] = element['name']
            for coord in element['xyz']:
                element_array.append(float("{:.5f}".format(coord)))
            coord_dict["value"] = element_array

            basis_elements.append(atom_dict)
            basis_coordinates.append(coord_dict)

        centered_basis['elements'] = basis_elements
        centered_basis['name'] = "atomic_coordinates"
        centered_basis['values'] = basis_coordinates

        return centered_basis
