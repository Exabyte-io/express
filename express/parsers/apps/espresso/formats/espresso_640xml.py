from typing import List, Dict, Union

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
