import re

from express.parsers.settings import GENERAL_REGEX

COMMON_REGEX = r"{}\s+[=:<>]\s*([-+]?\d*\.?\d*([Ee][+-]?\d+)?)"
DOUBLE_REGEX = GENERAL_REGEX["double_number"]
NWCHEM_OUTPUT_FILE_REGEX = "Northwest Computational Chemistry Package"

GEOMETRY_HEADER_REGEX = r"Output coordinates in (?P<units>\S+) \(scale by\s+(?P<scale>[\d.]+) to convert to a\.u\.\)"
# Requiring the tag to start with a symbol keeps a numeric-looking row of another table from matching.
ELEMENT_REGEX = r"[A-Za-z]+"
GEOMETRY_TAG_REGEX = r"{}\S*".format(ELEMENT_REGEX)
GEOMETRY_RULE_REGEX = r"^[ \t]*-{4,}[- \t]*$\n"
GEOMETRY_ROW_TEMPLATE = r"^[ \t]*\d+[ \t]+{tag}[ \t]+{double}[ \t]+{x}[ \t]+{y}[ \t]+{z}[ \t]*$"
# Never across the next block, so a header is always paired with its own table.
UNTIL_NEXT_GEOMETRY_REGEX = r"(?:(?!Output coordinates in)[\s\S])*?"

# The trailing `(?:row)+` bounds the table: it stops at the blank line after the last atom.
GEOMETRY_BLOCK_REGEX = re.compile(
    GEOMETRY_HEADER_REGEX
    + UNTIL_NEXT_GEOMETRY_REGEX
    + GEOMETRY_RULE_REGEX
    + r"(?P<rows>(?:{})+)".format(
        GEOMETRY_ROW_TEMPLATE.format(
            tag=GEOMETRY_TAG_REGEX, double=DOUBLE_REGEX, x=DOUBLE_REGEX, y=DOUBLE_REGEX, z=DOUBLE_REGEX
        )
        + r"\n"
    ),
    re.MULTILINE,
)
GEOMETRY_ROW_REGEX = re.compile(
    GEOMETRY_ROW_TEMPLATE.format(
        tag=r"(?P<element>{})\S*".format(ELEMENT_REGEX),
        double=DOUBLE_REGEX,
        x=r"(?P<x>{})".format(DOUBLE_REGEX),
        y=r"(?P<y>{})".format(DOUBLE_REGEX),
        z=r"(?P<z>{})".format(DOUBLE_REGEX),
    ),
    re.MULTILINE,
)

# Closed-shell runs print a single unlabeled section, spin-polarized (ODFT) ones an Alpha and a Beta.
ORBITAL_ANALYSIS_BLOCK_REGEX = re.compile(r"DFT Final (?:(?P<spin>Alpha|Beta) )?Molecular Orbital Analysis")
VECTOR_REGEX = re.compile(
    r"Vector\s+(?P<vector>\d+)\s+Occ=\s*(?P<occupation>[\dDEe.+-]+)\s+E=\s*(?P<energy>[\dDEe.+-]+)"
)

REGEX = {
    "total_energy": {"regex": COMMON_REGEX.format("Total DFT energy"), "occurrences": -1, "output_type": "float"},
    "zero_point_energy": {
        "regex": COMMON_REGEX.format("Zero-Point correction to Energy"),
        "occurrences": -1,
        "output_type": "float",
    },
    "thermal_correction_to_energy": {
        "regex": COMMON_REGEX.format("Thermal correction to Energy"),
        "occurrences": -1,
        "output_type": "float",
    },
    "thermal_correction_to_enthalpy": {
        "regex": COMMON_REGEX.format("Thermal correction to Enthalpy"),
        "occurrences": -1,
        "output_type": "float",
    },
}
TOTAL_ENERGY_CONTRIBUTIONS = {
    "one_electron": {"regex": COMMON_REGEX.format("One electron energy"), "occurrences": -1, "output_type": "float"},
    "coulomb": {"regex": COMMON_REGEX.format("Coulomb Energy"), "occurrences": -1, "output_type": "float"},
    "exchange_correlation": {
        "regex": COMMON_REGEX.format("Exchange-Corr. energy"),
        "occurrences": -1,
        "output_type": "float",
    },
    "nuclear_repulsion": {
        "regex": COMMON_REGEX.format("Nuclear repulsion energy"),
        "occurrences": -1,
        "output_type": "float",
    },
}
