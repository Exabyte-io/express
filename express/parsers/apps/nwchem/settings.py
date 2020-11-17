from express.parsers.settings import GENERAL_REGEX

NWCHEM_OUT_FILE_SUFFIX = ".log"

# regex = regular expression
COMMON_REGEX = r"{0}\s+[=:<>]\s*([-+]?\d*\.?\d*([Ee][+-]?\d+)?)"
DOUBLE_REGEX = GENERAL_REGEX.double_number

REGEX = {
    "total": {
        "regex": r"Total DFT energy\s+=\s+(\d+)",
        "output_type": "float",
    }
}
TOTAL_ENERGY_CONTRIBUTIONS = {
    "one_electron": {
        "regex": COMMON_REGEX.format("One electron energy"),
        "start_flag": "!",
        "occurrences": -1,
        "output_type": "float"
    },
    "coulomb": {
        "regex": COMMON_REGEX.format("Coulomb Energy"),
        "start_flag": "!",
        "occurrences": -1,
        "output_type": "float"
    },
    "exchange_correlation": {
        "regex": COMMON_REGEX.format("Exchange-Corr. energy"),
        "start_flag": "!",
        "occurrences": -1,
        "output_type": "float"
    },
    "nuclear_repulsion": {
        "regex": COMMON_REGEX.format("Nuclear repulsion energy"),
        "start_flag": "!",
        "occurrences": -1,
        "output_type": "float"
    }
}
