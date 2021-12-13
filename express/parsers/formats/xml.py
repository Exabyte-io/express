import os
import xml.etree.ElementTree as ET
from typing import Sequence, Optional, Any


def string_to_vec(string: str,
                  dtype: type = float,
                  container: type = list,
                  sep: Optional[str] = None) -> Sequence[Any]:
    """
    Given a string and some delimiter, will create a vector with the specified type.

    Args:
        string (str): The string to convert, for example "6.022e23 2.718 3.14159"
        dtype (type): The type to convert into. Must support conversion from a string. Defaults to `float`
        container (type): The container that will store the vector (e.g. a list, a numpy array, etc). Assumes an
                          interface where the container's constructor can take a list as an argument.
        sep (Optional[str]): Delimiter for the the string. Defaults to whitespace.
    Returns:
        List[Any]: A list that has the correct type, for example [6.022e23, 2.718, 3.14159]
    """
    result = [dtype(component) for component in string.split(sep)]
    result = container(result)
    return result


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
