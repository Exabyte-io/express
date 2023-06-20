from express.parsers.settings import GENERAL_REGEX

COMMON_REGEX = r"{}\s+[=:<>]\s*([-+]?\d*\.?\d*([Ee][+-]?\d+)?)"
DOUBLE_REGEX = GENERAL_REGEX.double_number
NWCHEM_OUTPUT_FILE_REGEX = "Northwest Computational Chemistry Package"

REGEX = {"total_energy": {"regex": COMMON_REGEX.format("Total DFT energy"), "occurrences": -1, "output_type": "float"}}
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
