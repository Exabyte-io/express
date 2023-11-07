import re
from abc import abstractmethod

import numpy as np

from express.parsers.formats.xml import BaseXMLParser
from express.parsers.settings import GENERAL_REGEX, Constant


class EspressoXMLParserBase(BaseXMLParser):
    """
    Base Espresso XML parser class.

    Args:
        xml_file_path (str): path to the xml file.
    """

    TAG_VALUE_CAST_MAP = {
        "character": lambda v, s, c: v,
        "integer": lambda v, s, c: np.array([int(_) for _ in re.findall(GENERAL_REGEX.int_number, v)]).reshape(
            [s // c, c]
        ),
        "real": lambda v, s, c: np.array([float(_) for _ in re.findall(GENERAL_REGEX.double_number, v)]).reshape(
            [s // c, c]
        ),
        "logical": lambda v, s, c: False if v in ["F", "false"] else True,
    }

    band_structure_tag = "BAND_STRUCTURE_INFO"
    fermi_energy_tag = "FERMI_ENERGY"
    lattice_tag = "DIRECT_LATTICE_VECTORS"
    reciprocal_lattice_tag = "RECIPROCAL_LATTICE_VECTORS"

    def __init__(self, xml_file_path):
        super().__init__(xml_file_path)

    def _get_xml_tag_value(self, tag):
        """
        This function helps casting xml tag value to the the type defined in the tag attribute. It xml tag's text
        holds a string, vector, (vector, matrix, constant) of either int or float.

        Args:
            tag (xml.etree.ElementTree.Element): An Element instance of ElementTree XML class.

        Returns:
            str | float | int | bool | ndarray: depending on the tag type attribute.
        """
        type = tag.attrib.get("type")
        size = int(tag.attrib.get("size", 1))
        columns = int(tag.attrib.get("columns", 1))
        result = self.TAG_VALUE_CAST_MAP[type](tag.text, size, columns)
        return result[0][0] if size == 1 and type not in ["logical", "character"] else result

    def fermi_energy(self):
        """
        Extracts fermi energy.

        Returns:
            float
        """
        bs_tag = self.root.find(self.band_structure_tag)
        return self._get_xml_tag_value(bs_tag.find(self.fermi_energy_tag)) * Constant.HARTREE

    @abstractmethod
    def nspins(self) -> int:
        """
        Extracts the number of number of spin components.

        Returns:
             int
        """
        pass

    @abstractmethod
    def final_lattice_vectors(self, reciprocal=False) -> dict:
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
        pass

    def get_inverse_reciprocal_lattice_vectors(self):
        """
        Returns inverse reciprocal lattice vectors to convert cartesian (2pi/a) point to crystal.
        """
        reciprocal_lattice = self.final_lattice_vectors(reciprocal=True)
        lattice_array = [reciprocal_lattice["vectors"][i] for i in ["a", "b", "c"]]
        return np.linalg.inv(np.array(lattice_array))

    @abstractmethod
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
        pass

    @abstractmethod
    def final_basis(self):
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
        pass
