import os
from typing import Optional, Union

from express.parsers.apps.espresso import settings
from express.parsers.apps.espresso.formats.xml.xml_base import EspressoXMLParserBase
from express.parsers.apps.espresso.formats.xml.xml_post64 import EspressoXMLParserPostV6_4


def get_xml_parser(
    parser_version: Union[str, None], work_dir: str, is_sternheimer_gw: bool = False
) -> EspressoXMLParserBase:
    """
    Get XML parser for espresso. Only supports post-6.4 versions.
    
    Args:
        parser_version: Version string (unused, kept for compatibility)
        work_dir: Working directory
        is_sternheimer_gw: Whether this is a Sternheimer GW calculation
        
    Returns:
        EspressoXMLParserPostV6_4 instance
    """
    xml_file = find_xml_file(
        work_dir,
        settings.XML_DATA_FILE,
        is_sternheimer_gw,
    )
    return EspressoXMLParserPostV6_4(xml_file)


def find_xml_file(work_dir: str, default_xml_filename: str, is_sternheimer_gw: bool) -> Optional[str]:
    """
    Finds XML file.

    Note: Sternheimer GW XML file of the first process (gw0) is returned if this a Sternheimer GW calculation.

    Returns:
        str
    """
    for root, dirs, files in os.walk(work_dir, followlinks=True):
        for file_ in [f for f in files if default_xml_filename == f]:
            file_path = os.path.join(root, file_)
            if not is_sternheimer_gw or (is_sternheimer_gw and settings.STERNHEIMER_GW0_DIR_PATTERN in file_path):
                return file_path
