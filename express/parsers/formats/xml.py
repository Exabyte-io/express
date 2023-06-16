import os
import xml.etree.ElementTree as ET


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
            except ET.ParseError:
                # safely ignore broken xml file
                pass
