import re

from express.parsers.settings import GENERAL_REGEX

COMMON_REGEX = r"{}\s+[=:<>]\s*([-+]?\d*\.?\d*([Ee][+-]?\d+)?)"
DOUBLE_REGEX = GENERAL_REGEX["double_number"]
NWCHEM_OUTPUT_FILE_REGEX = "Northwest Computational Chemistry Package"

# Geometry blocks are printed in whichever units the input declared; `scale` converts them to a.u.
GEOMETRY_BLOCK_REGEX = re.compile(
    r"Output coordinates in (?P<units>\S+) \(scale by\s+(?P<scale>[\d.]+) to convert to a\.u\.\)"
)
# The element symbol is the leading alphabetic part of the geometry tag, e.g. "O", "H2" -> "H".
ELEMENT_FROM_TAG_REGEX = re.compile(r"^([A-Za-z]+)")
GEOMETRY_ROW_REGEX = re.compile(
    r"^[ \t]*\d+[ \t]+(?P<tag>\S+)[ \t]+{0}[ \t]+(?P<x>{0})[ \t]+(?P<y>{0})[ \t]+(?P<z>{0})[ \t]*$".format(
        DOUBLE_REGEX
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
