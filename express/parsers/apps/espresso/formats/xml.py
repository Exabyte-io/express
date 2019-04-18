from __future__ import absolute_import

import os
import re
import string
import numpy as np
import xml.etree.ElementTree as ET

from express.parsers.settings import Constant
from express.parsers.settings import GENERAL_REGEX
from express.parsers.formats.xml import BaseXMLParser

TAG_VALUE_CAST_MAP = {
    'character': lambda v, s, c: v,
    'integer': lambda v, s, c: np.array([int(_) for _ in re.findall(GENERAL_REGEX.int_number, v)]).reshape([s / c, c]),
    'real': lambda v, s, c: np.array([float(_) for _ in re.findall(GENERAL_REGEX.double_number, v)]).reshape([s / c, c]),
    'logical': lambda v, s, c: False if 'F' in v else True

}


class EspressoXMLParser(BaseXMLParser):
    """
    Espresso XML parser class.

    Args:
        xml_file_path (str): path to the xml file.
    """

    def __init__(self, xml_file_path):
        super(EspressoXMLParser, self).__init__(xml_file_path)

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
        result = TAG_VALUE_CAST_MAP[type](tag.text, size, columns)
        return result[0][0] if size == 1 and type not in ['logical', 'character'] else result

    def fermi_energy(self):
        """
        Extracts fermi energy.

        Returns:
            float
        """
        bs_tag = self.root.find("BAND_STRUCTURE_INFO")
        return self._get_xml_tag_value(bs_tag.find("FERMI_ENERGY")) * Constant.HARTREE

    def nspins(self):
        """
        Extracts the number of number of spin components.

        Returns:
             int
        """
        bs_tag = self.root.find("BAND_STRUCTURE_INFO")
        return self._get_xml_tag_value(bs_tag.find("NUMBER_OF_SPIN_COMPONENTS"))

    def final_lattice_vectors(self, reciprocal=False):
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
        vector_tag = 'a'
        lattice_tag = 'DIRECT_LATTICE_VECTORS'
        units_tag = 'UNITS_FOR_DIRECT_LATTICE_VECTORS'

        if reciprocal:
            vector_tag = 'b'
            lattice_tag = 'RECIPROCAL_LATTICE_VECTORS'
            units_tag = 'UNITS_FOR_RECIPROCAL_LATTICE_VECTORS'

        vectors = {}
        cell_tag = self.root.find("CELL")
        lattice_units_tag = cell_tag.find(lattice_tag).find(units_tag)
        for vector in cell_tag.find(lattice_tag):
            if vector.tag.startswith(vector_tag):
                vectors.update({
                    string.ascii_lowercase[int(vector.tag[1]) - 1]: (
                        (Constant.BOHR if not reciprocal else 1.0) * self._get_xml_tag_value(vector)[0]).tolist()
                })
        vectors.update({'alat': 1.0})
        return {'vectors': vectors, 'units': 'angstrom'} if not reciprocal else {'vectors': vectors}

    def get_inverse_reciprocal_lattice_vectors(self):
        """
        Returns inverse reciprocal lattice vectors to convert cartesian (2pi/a) point to crystal.
        """
        reciprocal_lattice = self.final_lattice_vectors(reciprocal=True)
        lattice_array = [reciprocal_lattice['vectors'][i] for i in ['a', 'b', 'c']]
        return np.linalg.inv(np.array(lattice_array))

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
        eigenvalues_at_kpoints = []
        for eigenvalue_tag in self.root.find("EIGENVALUES"):
            cartesianKPoint = self._get_xml_tag_value(eigenvalue_tag.find("K-POINT_COORDS"))[0]
            crystalKPoint = np.dot(cartesianKPoint, self.get_inverse_reciprocal_lattice_vectors())
            eigenvalues_at_kpoint = {
                "kpoint": crystalKPoint.tolist(),
                "weight": self._get_xml_tag_value(eigenvalue_tag.find("WEIGHT")),
                "eigenvalues": []
            }
            for datafile_tag in [t for t in eigenvalue_tag.iter() if t.tag.startswith('DATAFILE')]:
                eigenval_file = os.path.join(self.xml_dir_name, datafile_tag.attrib.get("iotk_link"))
                energies, occupations = self._parse_eigenvalue_file(eigenval_file)
                eigenvalues_at_kpoint['eigenvalues'].append({
                    'energies': (np.array(energies) * Constant.HARTREE).tolist(),
                    'occupations': occupations,
                    'spin': 0.5 if datafile_tag.tag in ['DATAFILE', 'DATAFILE.1'] else -0.5
                })
            eigenvalues_at_kpoints.append(eigenvalues_at_kpoint)
        return eigenvalues_at_kpoints

    def _parse_eigenvalue_file(self, eigenval_xml_path):
        """
        Extracts eigenvalues from a given file.

        Args:
            eigenval_xml_path (str): path to eigenvalue xml file.

        Returns:
            tuple: (energies, occupations)
        """
        root = ET.parse(eigenval_xml_path).getroot()
        energies = [float(_) for _ in re.findall(GENERAL_REGEX.double_number, root.find('EIGENVALUES').text)]
        occupations = [float(_) for _ in re.findall(GENERAL_REGEX.double_number, root.find('OCCUPATIONS').text)]
        return energies, occupations

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
        elements, coordinates = [], []
        ion_tag = self.root.find("IONS")
        for atom in ion_tag:
            if atom.tag.startswith("ATOM"):
                elements.append({
                    'id': int(atom.tag[5:]),
                    'value': atom.attrib.get("SPECIES").strip(' \t\n\r')
                })
                coordinates.append({
                    'id': int(atom.tag[5:]),
                    'value': (Constant.BOHR * np.array(atom.attrib.get("tau").split()).astype(np.float)).tolist()
                })

        return {
            'units': 'angstrom',
            'elements': elements,
            'coordinates': coordinates
        }
