import os
import re
import string
import numpy as np
import xml.etree.ElementTree as ET

from express.parsers.settings import Constant
from express.parsers.settings import GENERAL_REGEX
from express.parsers.apps.espresso.formats.espresso_legacyxml import TAG_VALUE_CAST_MAP
from express.parsers.formats.xml import BaseXMLParser


def find_tag(node, tag):
    """
    DFS for tag in the node tree
    """
    if node.tag == tag:
        return node

    for child in node:
        result = find_tag(child, tag)
        if result is not None:
            return result


class Espresso640XMLParser(BaseXMLParser):
    """
    Espresso XML parser class.

    Args:
        xml_file_path (str): path to the xml file.`
    """

    def _get_step_by_index(self, index):
        steps = sorted(self.root.findall('step'), key=lambda node: int(node.get('n_step')))
        return steps[index]

    def fermi_energy(self) -> float:
        fermi_node = find_tag(self.root, 'fermi_energy')
        result = float(fermi_node.text) * Constant.HARTREE
        return result

    def nspins(self):
        # TODO: How is this defined in the current version of Espresso? Seems to be missing from their schema
        raise NotImplementedError()

    def get_inverse_reciprocal_lattice_vectors(self):
        raise NotImplementedError

    def eigenvalues_at_kpoints(self):
    #     bs_node = find_tag(self.root, 'band_structure')
    #     ks_nodes = bs_node.find_all('ks_energies')
        raise NotImplementedError

    def final_basis(self):
        raise NotImplementedError


    def final_lattice_vectors(self, reciprocal=False):
        if reciprocal:
            raise NotImplementedError

        vectors = {}
        final_step = self._get_step_by_index(-1)
        cell = final_step.find('cell')
        # TODO: Check what the units actually are here, to make sure we need to do this conversion
        for output_label, xml_label in (("a", "a1"), ("b", "a2"), ("c", "a3")):
            vector = map(float, cell.find(xml_label).split())
            vectors[output_label] = [component * Constant.BOHR for component in vector]
