from express.parsers.settings import GENERAL_REGEX

PDOS_TOT_FILE = "pdos_tot"
XML_DATA_FILE = "data-file.xml"

_COMMON_REGEX = r"{0}\s+[=:<>]\s*([-+]?\d*\.?\d*([Ee][+-]?\d+)?)"

REGEX = {
    "total_energy": {
        "regex": _COMMON_REGEX.format("total energy"),
        "start_flag": "!",
        "occurrences": -1,
        "output_type": "float"
    },
    "pdos_file": {
        "regex": r'.*\.pdos_atm#(?P<atom_num>\d+)\((?P<atom_name>\w+)\)'
                 r'_wfc#(?P<orbit_num>\d+)\((?P<orbit_symbol>\w)\)',
    },
    "convergence_electronic": {
        "regex": r"estimated scf accuracy\s+<\s+({0})".format(GENERAL_REGEX.double_number),
        "output_type": "float",
    },
    "convergence_ionic": {
        "regex": r"total energy\s+=\s+({0})".format(GENERAL_REGEX.double_number),
        "output_type": "float",
    },
    "bfgs_block": {
        "regex": r"new unit-cell volume.+?Writing output data file",
    },
    "lattice": {
        "regex": (
            r"CELL_PARAMETERS\s+\(alat=\s+({0})\)"
            r"\s+({0})\s+({0})\s+({0})"
            r"\s+({0})\s+({0})\s+({0})"
            r"\s+({0})\s+({0})\s+({0})"
        ).format(GENERAL_REGEX.double_number)
    },
    "ion_position": {
        "regex": r"([A-Z][a-z]?)\s+({0})\s+({0})\s+({0})".format(GENERAL_REGEX.double_number)
    },
    "stress_tensor": {
        "regex": r"^\s*({0})\s+({0})\s+({0}) +{0}\s+{0}\s+{0}".format(GENERAL_REGEX.double_number),
        "start_flag": "entering subroutine stress ...",
        "occurrences": 3,
        "output_type": "float",
        "match_groups": [1, 2, 3]
    },
    "pressure": {
        "regex": r"\s*total\s+stress\s+\(Ry/bohr\*\*3\)\s*\(kbar\)\s*P=\s*({0})".format(GENERAL_REGEX.double_number),
        "start_flag": "entering subroutine stress",
        "occurrences": -1,
        "output_type": "float"
    },
    "total_force": {
        "regex": _COMMON_REGEX.format("Total force"),
        "start_flag": "Total force",
        "occurrences": -1,
        "output_type": "float"
    },
    "forces_on_atoms": {
        "regex": r"^\s*atom\s+\d+\s+type\s+\d+\s+force\s+=\s+({0})\s+({0})\s+({0})".format(GENERAL_REGEX.double_number),
        "start_flag": "Forces acting on atoms (Ry/au):",
        "occurrences": 0,
        "output_type": "float",
        "match_groups": [1, 2, 3]
    },
    "zero_point_energy": {
        "regex": r"freq\s\(\s+\d+\)\s+\=\s+\d+\.\d+\s+\[THz\]\s+\=\s+({0})\s+\[cm\-1\]".format(GENERAL_REGEX.double_number),
        "start_flag": "Diagonalizing the dynamical matrix",
        "output_type": "float"
    }
}

TOTAL_ENERGY_CONTRIBUTIONS = {
    "harris_foulkes": {
        "regex": _COMMON_REGEX.format("Harris-Foulkes estimate"),
        "start_flag": "!",
        "occurrences": -1,
        "output_type": "float"
    },
    "one_electron": {
        "regex": _COMMON_REGEX.format("one-electron contribution"),
        "start_flag": "!",
        "occurrences": -1,
        "output_type": "float"
    },
    "hartree": {
        "regex": _COMMON_REGEX.format("hartree contribution"),
        "start_flag": "!",
        "occurrences": -1,
        "output_type": "float"
    },
    "exchange_correlation": {
        "regex": _COMMON_REGEX.format("xc contribution"),
        "start_flag": "!",
        "occurrences": -1,
        "output_type": "float"
    },
    "ewald": {
        "regex": _COMMON_REGEX.format("ewald contribution"),
        "start_flag": "!",
        "occurrences": -1,
        "output_type": "float"
    },
    "smearing": {
        "regex": _COMMON_REGEX.format("smearing contrib\.\s+\(-TS\)"),
        "start_flag": "!",
        "occurrences": -1,
        "output_type": "float"
    }
}
