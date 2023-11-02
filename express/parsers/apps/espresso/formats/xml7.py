from typing import Union
from xml.etree.ElementTree import Element

import numpy as np

from express.parsers.settings import Constant

from .xml import EspressoXMLParser


class EspressoXMLParserV7(EspressoXMLParser):
    """
    XML parser overrides for espresso >= v7.

    QE7.2 XML output does not contain the type, size, (len/columns) attributes so the parser is not as generalizable.
    """

    band_structure_tag = "band_structure"
    fermi_energy_tag = "fermi_energy"
    lattice_tag = "cell"
    reciprocal_lattice_tag = "reciprocal_lattice"

    # maps the tag name to the expected format, which we use the base class formatter to extract
    EXACT_MATCH_FMT_MAP = {
        fermi_energy_tag: {
            "type_": "real",
            "size": 1,
            "columns": 1,
        },
        "lsda": {
            "type_": "logical",
            "size": 1,
            "columns": 1,
        },
        "noncolin": {
            "type_": "logical",
            "size": 1,
            "columns": 1,
        },
        "k_point": {
            "type_": "real",
            "size": 3,
            "columns": 3,
        },
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = self.root.find("output") if self.root else None

    def nspins(self) -> int:
        bs_tag = self.root.find(self.band_structure_tag)
        lsda_tag = self._get_xml_tag_value(bs_tag.find("lsda"))
        noncolin_tag = self._get_xml_tag_value(bs_tag.find("noncolin"))

        if lsda_tag:
            return 2
        elif noncolin_tag:
            return 4

        return 1

    def final_lattice_vectors(self, reciprocal=False):
        """
        Extract lattice vectors

        Args:
            reciprocal (bool, optional): Whether to extract reciprocal lattice. Defaults to False.

        Returns:
            dict: lattice vectors
        {
            "vectors: {
                "a": [float, float, float],
                "b": [float, float, float],
                "c": [float, float, float],
                "alat": float
            }
            Optional["units": "angstrom"]
        }
        """
        vectors = {}
        structure = self.root.find("atomic_structure")
        lattice_constant = structure.attrib.get("alat", 1)

        if reciprocal:
            # use basis_set tag as atomic structure tag does not contain reciprocal lattice
            lattice = self.root.find("basis_set").find(self.reciprocal_lattice_tag)
            constant = 1.0
        else:
            lattice = structure.find(self.lattice_tag)
            constant = Constant.BOHR
            vectors.update({"units": "angstrom"})

        values = np.array([[float(v) for v in vector.text.split()] for vector in lattice]) * constant
        vectors.update(
            {
                "vectors": {
                    "a": values[0].tolist(),
                    "b": values[1].tolist(),
                    "c": values[2].tolist(),
                    "alat": float(lattice_constant) * constant,
                }
            }
        )

        return vectors

    def eigenvalues_at_kpoints(self) -> list:
        """
        Return list of eigenvalue data for all kpoints.

        Returns:
            list: [
                {
                    "kpoint": [float, float, float],
                    "weight": "float",
                    "eigenvalues": [
                        {
                            "energies": [float, ..., float],
                            "occupations": [float, ..., float],
                            "spin": float(0.5 or -0.5)
                        }
                    ]
                }
            ]
        """
        all_kpoints = []
        bs_tag = self.root.find(self.band_structure_tag)
        for ks_entry in bs_tag.iterfind("ks_energies"):
            all_kpoints.append(self.__process_ks_energies(ks_entry))
        return all_kpoints

    def __process_ks_energies(self, ks_entry: Element) -> dict:
        """Process a single ks_energies tag, under band_structure tag"""
        k_point = ks_entry.find("k_point")
        cartesian_coords = self._get_xml_tag_value(k_point)[0]
        crystal_coords = np.dot(cartesian_coords, self.get_inverse_reciprocal_lattice_vectors())
        kpoint_dict = {
            "kpoint": crystal_coords.tolist(),
            "weight": float(k_point.attrib.get("weight")),
            "eigenvalues": [],
        }
        # TODO: previous format has (potentially) multiple linked datafiles. What is the equivalent now?
        kpoint_dict["eigenvalues"].append(
            {
                "energies": [float(eigenvalue) for eigenvalue in ks_entry.find("eigenvalues").text.split()],
                "occupations": [float(occ) for occ in ks_entry.find("occupations").text.split()],
                "spin": 0.5,  # TODO: where does this come from in the new datafile format?
            }
        )

        return kpoint_dict

    def final_basis(self) -> dict:
        elements, coordinates = [], []
        atomic_positions = self.root.find("atomic_structure").find("atomic_positions")
        for atom in atomic_positions.iterfind("atom"):
            elements.append(
                {
                    "id": int(atom.attrib.get("index")),
                    "value": atom.attrib.get("name"),
                }
            )
            coordinates.append(
                {
                    "id": int(atom.attrib.get("index")),
                    "value": (Constant.BOHR * np.array(atom.text.split()).astype(np.float32)).tolist(),
                }
            )
        return {"units": "angstrom", "elements": elements, "coordinates": coordinates}

    def _get_xml_tag_value(self, tag: Element) -> Union[str, float, int, bool, np.ndarray]:
        """
        Returns the value of a given xml tag. QE7.2 XML does not contain the type attribute.

        Args:
            tag (xml.etree.ElementTree.Element): The final nested Element that we are getting value from
            type


        Returns:
            _type_: _description_
        """
        fmt_dict = self.EXACT_MATCH_FMT_MAP[tag.tag]
        type_, size, columns = [fmt_dict.get(k) for k in ["type_", "size", "columns"]]
        result = self.TAG_VALUE_CAST_MAP[type_](tag.text, size, columns)
        return result[0][0] if size == 1 and type_ not in ["logical", "character"] else result
