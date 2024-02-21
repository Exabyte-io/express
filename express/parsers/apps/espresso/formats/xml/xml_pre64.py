import os
import re
import string
import xml.etree.ElementTree as ET

import numpy as np

from express.parsers.apps.espresso.formats.xml.xml_base import EspressoXMLParserBase
from express.parsers.settings import GENERAL_REGEX, Constant


class EspressoXMLParserPreV6_4(EspressoXMLParserBase):
    """
    Espresso XML parser class for versions <= v6.4.

    Args:
        xml_file_path (str): path to the xml file.
    """

    band_structure_tag = "BAND_STRUCTURE_INFO"
    fermi_energy_tag = "FERMI_ENERGY"
    lattice_tag = "DIRECT_LATTICE_VECTORS"
    reciprocal_lattice_tag = "RECIPROCAL_LATTICE_VECTORS"

    def __init__(self, xml_file_path):
        super().__init__(xml_file_path)

    def fermi_energy(self):
        """
        Extracts fermi energy.

        Returns:
            float
        """
        bs_tag = self.root.find(self.band_structure_tag)
        return self._get_xml_tag_value(bs_tag.find(self.fermi_energy_tag)) * Constant.HARTREE

    def nspins(self):
        """
        Extracts the number of number of spin components.

        Returns:
             int
        """
        bs_tag = self.root.find(self.band_structure_tag)
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
        vector_tag = "a"
        lattice_tag = self.lattice_tag

        if reciprocal:
            vector_tag = "b"
            lattice_tag = self.reciprocal_lattice_tag

        vectors = {}
        cell_tag = self.root.find("CELL")
        # lattice_units_tag = cell_tag.find(lattice_tag).find(units_tag)
        for vector in cell_tag.find(lattice_tag):
            if vector.tag.startswith(vector_tag):
                vectors.update(
                    {
                        string.ascii_lowercase[int(vector.tag[1]) - 1]: (
                            (Constant.BOHR if not reciprocal else 1.0) * self._get_xml_tag_value(vector)[0]
                        ).tolist()
                    }
                )
        vectors.update({"alat": 1.0})
        return {"vectors": vectors, "units": "angstrom"} if not reciprocal else {"vectors": vectors}

    def get_inverse_reciprocal_lattice_vectors(self):
        """
        Returns inverse reciprocal lattice vectors to convert cartesian (2pi/a) point to crystal.
        """
        reciprocal_lattice = self.final_lattice_vectors(reciprocal=True)
        lattice_array = [reciprocal_lattice["vectors"][i] for i in ["a", "b", "c"]]
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
                "eigenvalues": [],
            }
            for datafile_tag in [t for t in eigenvalue_tag.iter() if t.tag.startswith("DATAFILE")]:
                eigenval_file = os.path.join(self.xml_dir_name, datafile_tag.attrib.get("iotk_link"))
                energies, occupations = self._parse_eigenvalue_file(eigenval_file)
                eigenvalues_at_kpoint["eigenvalues"].append(
                    {
                        "energies": (np.array(energies) * Constant.HARTREE).tolist(),
                        "occupations": occupations,
                        "spin": 0.5 if datafile_tag.tag in ["DATAFILE", "DATAFILE.1"] else -0.5,
                    }
                )
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
        energies = [float(_) for _ in re.findall(GENERAL_REGEX.double_number, root.find("EIGENVALUES").text)]
        occupations = [float(_) for _ in re.findall(GENERAL_REGEX.double_number, root.find("OCCUPATIONS").text)]
        return energies, occupations

    def final_basis(self):
        """
        Extracts basis.

        Returns:
            dict

        Example:
            {
                'units': 'angstrom',
                'elements': [{'id': 0, 'value': 'Si'}, {'id': 1, 'value': 'Si'}],
                'coordinates': [{'id': 0, 'value': [0.0, 0.0, 0.0]}, {'id': 1, 'value': [0.0, 0.0, 0.0]}]
             }
        """
        elements, coordinates = [], []
        ion_tag = self.root.find("IONS")
        for atom in ion_tag:
            if atom.tag.startswith("ATOM"):
                elements.append({"id": int(atom.tag[5:]), "value": atom.attrib.get("SPECIES").strip(" \t\n\r")})
                coordinates.append(
                    {
                        "id": int(atom.tag[5:]),
                        "value": (Constant.BOHR * np.array(atom.attrib.get("tau").split()).astype(np.float32)).tolist(),
                    }
                )

        return {"units": "angstrom", "elements": elements, "coordinates": coordinates}
