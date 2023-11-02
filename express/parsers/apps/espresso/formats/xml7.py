from typing import Any
from xml.etree.ElementTree import Element

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
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #
        self.root = self.root.find("output")

    def nspins(self):
        bs_tag = self.root.find(self.band_structure_tag)
        lsda_tag = bs_tag.find("lsda")
        noncolin_tag = bs_tag.find("noncolin")
        result = 1
        if lsda_tag is not False:
            result = 2
        elif noncolin_tag is not False:
            result = 4
        return result

    def _get_xml_tag_value(self, tag: Element, **kwargs) -> Any:
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
