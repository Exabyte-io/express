import os
import xml.etree.ElementTree as ET
from typing import Sequence


class BaseXMLParser(object):
    """
    Base XML parser class.
    """

    def __init__(self, xml_file_path):
        self.xml_path = xml_file_path
        self.root = None
        self.xml_dir_name = None
        if self.xml_path and os.path.exists(self.xml_path):
            try:
                self.xml_dir_name = os.path.dirname(self.xml_path)
                self.root = ET.parse(self.xml_path).getroot()
            except:
                # safely ignore broken xml file
                pass

    @staticmethod
    def traverse_xml(node: ET.Element, pathway: Sequence[str]) -> ET.Element:
        """
        Goes to a node in the node's path. For example, if we have a node tree that looks like A->B->C->D, then
        we could call go_to_node(B, ["C", "D"]) to return a reference to node D. Mostly this is useful to avoid numerous
        calls to "node.find('some_tag').find('some_other_tag').find('yet-another-tag')".
        """
        if isinstance(pathway, str):
            pathway = (pathway,)
        for step in pathway:
            node = node.find(step)
        return node
