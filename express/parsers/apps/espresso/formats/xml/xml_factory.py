import os
from typing import Optional, Union

from packaging import version

from express.parsers.apps.espresso import settings
from express.parsers.apps.espresso.formats.xml.xml_base import EspressoXMLParserBase
from express.parsers.apps.espresso.formats.xml.xml_post64 import EspressoXMLParserPostV6_4
from express.parsers.apps.espresso.formats.xml.xml_pre64 import EspressoXMLParserPreV6_4

VERSIONS = {
    "Pre6_4": {
        "parser": EspressoXMLParserPreV6_4,
        "default_xml_file": settings.XML_DATA_FILE_PREv6_4,
    },
    "Post6_4": {
        "parser": EspressoXMLParserPostV6_4,
        "default_xml_file": settings.XML_DATA_FILE_POSTv6_4,
    },
}


def get_xml_parser(
    parser_version: Union[str, None], work_dir: str, is_sternheimer_gw: bool = False
) -> EspressoXMLParserBase:
    parser_version = "6.4" if not parser_version else parser_version
    if version.parse(parser_version) <= version.parse("6.4"):
        version_key = "Pre6_4"
    else:
        version_key = "Post6_4"

    xml_file = find_xml_file(
        work_dir,
        VERSIONS[version_key]["default_xml_file"],
        is_sternheimer_gw,
    )
    return VERSIONS[version_key]["parser"](xml_file)


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
