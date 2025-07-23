import re

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



    def get_inverse_reciprocal_lattice_vectors(self):
        """
        Returns inverse reciprocal lattice vectors to convert cartesian (2pi/a) point to crystal.
        """
        reciprocal_lattice = self.final_lattice_vectors(reciprocal=True)
        lattice_array = [reciprocal_lattice["vectors"][i] for i in ["a", "b", "c"]]
        return np.linalg.inv(np.array(lattice_array))


