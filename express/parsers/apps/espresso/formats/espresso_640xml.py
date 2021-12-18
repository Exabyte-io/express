from typing import List, Dict, Union

import numpy as np

from express.parsers.formats.xml import BaseXMLParser
from express.parsers.utils import string_to_vec
from express.parsers.settings import Constant


class Espresso640XMLParser(BaseXMLParser):
    """
    Espresso XML parser class.
    Based on the schema at www.quantum-espresso.org/ns/qes/qes_210716.xsd
    Args:
        xml_file_path (str): path to the xml file.`
    """

    def __init__(self, xml_file_path):
        super().__init__(xml_file_path)
        self._steps = None

    @property
    def steps(self):
        if self._steps is None:
            self._steps = sorted(self.root.findall("step"), key=lambda node: int(node.get("n_step")))
        return self._steps

    def fermi_energy(self) -> float:
        """
        Extracts fermi energy.

        Returns:
            float
        """
        fermi_node = self.traverse_xml(self.root, ("output", "band_structure", "fermi_energy"))
        result = float(fermi_node.text) * Constant.HARTREE
        return result

    def nspins(self):
        """
        Extracts the number of number of spin components.
        Unfortunately, due to changes in the XML we can no longer directly get this. We can only indirectly infer it
        based on what the values of LSDA and Noncolin are.

        The alternative is to assume that we have an input file and write a parser for the input file, since that will
        have the actual number of spins specified.

        Returns:
             int
        """
        spin_input_node = self.traverse_xml(self.root, ("input", "spin"))
        is_lsda = spin_input_node.find("lsda").text == "true"
        is_noncolin = spin_input_node.find("noncolin") == "true"

        if is_noncolin:
            nspin = 4
        elif is_lsda:
            nspin = 2
        else:
            nspin = 1

        return nspin

    def eigenvalues_at_kpoints(self):
        """
        Returns eigenvalues for all kpoints.

        Returns:
             list

        Example:
            [
                {
                    'kpoint': [-0.5, 0.5, 0.5],
                    'weight': 9.5238095E-002,
                    'eigenvalues': [
                        {
                            'energies': [-1.4498446E-001, ..., 4.6507387E-001],
                            'occupations': [1, ... , 0],
                            'spin': 0.5
                        }
                    ]
                },
                ...
            ]
        """

        # Determine if we have multiple spin states
        # We're doing it this way to avoid coupling to the `self.nspins()` behavior. If there are up/down bands, then
        # we know there are multiple spins. Otherwise, it only makes sense to treet it as having a single spin state.
        bandstructure_node = self.traverse_xml(self.root, ("output", "band_structure"))
        if bandstructure_node.find("nbnd_up"):
            has_multiple_bands = True
        else:
            has_multiple_bands = False

        kpoints = []
        for ks_energy_node in bandstructure_node.findall("ks_energies"):
            # Basic information about the kpoint
            kpoint = {}
            kpoint_node = ks_energy_node.find("k_point")
            cartesian_kpoint = string_to_vec(kpoint_node.text, container=np.ndarray),
            crystal_kpoint = np.dot(cartesian_kpoint, self.get_inverse_reciprocal_lattice_vectors())
            kpoint["kpoint"] = crystal_kpoint  # Coordinates
            kpoint["weight"] = float(kpoint_node.get("weight"))

            # Extract eigenvalues
            eigenvalue_text = ks_energy_node.find("eigenvalues").text
            occupation_text = ks_energy_node.find("occupations").text
            energies = [component * Constant.HARTREE for component in string_to_vec(eigenvalue_text)]
            occupations = string_to_vec(occupation_text, dtype=float)

            # Split into up/down spin if we need to
            # In the case of having multiple spins, the spin up states are listed before the spin down states, hence
            # the list slicing.
            if has_multiple_bands:
                nband_up = int(bandstructure_node.find("nbnd_up").text)
                eigenvalues_up = {
                    "energies": energies[0:nband_up],
                    "occupations": occupations[0:nband_up],
                    "spin": 0.5,
                }
                eigenvalues_down = {
                    "energies": energies[nband_up:-1],
                    "occupations": occupations[nband_up:-1],
                    "spin": -0.5,
                }
                eigenvalues = [eigenvalues_up, eigenvalues_down]
            else:
                eigenvalues = [{
                    "energies": energies,
                    "occupations": occupations,
                    "spin": 0.5,  # ToDo: Is this the value we expect for when there is only one spin?
                }]
            kpoint["eigenvalues"] = eigenvalues
            kpoints.append(kpoint)
        return kpoints

    def final_lattice_vectors(self, reciprocal=False) -> Dict[str, Dict[str, Union[float, List[float]]]]:
        """
        Extracts lattice.

        Args:
            reciprocal (bool): whether to extract reciprocal lattice.

        Returns:
            dict

        Examples:
            {
                'vectors': {
                    'a': [-0.561154473, -0.000000000, 0.561154473],
                    'b': [-0.000000000, 0.561154473, 0.561154473],
                    'c': [-0.561154473, 0.561154473, 0.000000000],
                    'alat': 9.44858082
                }
             }
        """
        vectors = {"alat": 1.0}
        result = {"vectors": vectors}
        if reciprocal:
            cell_node = self.traverse_xml(self.root, ("output", "basis_set", "reciprocal_lattice"))
            scale_factor = 1.0
            tags = ("b1", "b2", "b3")
        else:
            cell_node = self.traverse_xml(self.root, ("output", "atomic_structure", "cell"))
            scale_factor = Constant.BOHR
            tags = ("a1", "a2", "a3")
            result["units"] = "angstrom"

        for key, tag in zip(("a", "b", "c"), tags):
            vector = string_to_vec(cell_node.find(tag).text, dtype=float)
            vector = [component * scale_factor for component in vector]
            vectors[key] = vector

        return result

    def final_reciprocal_lattice_vectors(self) -> Dict[str, Dict[str, Union[float, List[float]]]]:
        """
        Convenient alias for final_lattice_vectors with reciprocal set to true
        """
        return self.final_lattice_vectors(reciprocal=True)

    def get_inverse_reciprocal_lattice_vectors(self) -> np.ndarray:
        """
        Computes the inverse reciprocal lattice vector
        """
        reciprocal_lattice = self.final_reciprocal_lattice_vectors()
        lattice_array = np.array([reciprocal_lattice['vectors'][i] for i in ('a', 'b', 'c')])
        inverted_lattice_array = np.linalg.inv(lattice_array)
        return inverted_lattice_array

    def final_basis(self) -> Dict[str, Union[str, Dict]]:
        """
        Extracts basis.

        Returns:
            dict

        Example:
            {
                'units': 'angstrom',
                'elements': [{'id': 1, 'value': 'Si'}, {'id': 2, 'value': 'Si'}],
                'coordinates': [{'id': 1, 'value': [0.0, 0.0, 0.0]}, {'id': 2, 'value': [0.0, 0.0, 0.0]}]
             }
        """
        result = {
            "units": "angstrom",
            "elements": [],
            "coordinates": []
        }
        output_positions = self.traverse_xml(self.root, ("output", "atomic_structure", "atomic_positions"))
        atoms = output_positions.findall("atom")
        for atom in atoms:
            atom_id = float(atom.get("index"))
            symbol = atom.get("name")
            coords = string_to_vec(atom.text, dtype=float)
            coords = [component * Constant.BOHR for component in coords]

            result["elements"].append({"id": atom_id, "value": symbol})
            result["coordinates"].append({"id": atom_id, "value": coords})

        return result
