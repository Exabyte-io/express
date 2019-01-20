from express.parsers.settings import GENERAL_REGEX

NEB_DIR_PREFIX = "0"
NEB_STD_OUT_FILE = "stdout"
XML_DATA_FILE = "vasprun.xml"

_COMMON_REGEX = r"{0}\s+({1})\s+({1})\s+({1})\s+({1})\s+({1})\s+({1})"

REGEX = {
    "total_energy": {
        "regex": r"F=\s+({0})".format(GENERAL_REGEX.double_number),
        "start_flag": "entering main loop",
        "occurrences": -1,
        "output_type": "float",
    },
    "ibz_kpoints": {
        "regex": r'({double})\s+({double})\s+({double})\s+{double}'.format(double=GENERAL_REGEX.double_number)
    },
    "convergence_electronic": {
        "regex": r".+:\s+(\d+)\s+{0}\s+({0})".format(GENERAL_REGEX.double_number),
        "output_type": "float",
        "match_groups": [1, 2]
    },
    "ion_positions_block": {
        "regex": r"POSITION.+?-{5,}\n(.+?)-{5,}"
    },
    "lattice_vectors": {
        "regex": r"direct lattice vectors.+\n"
                 r"\s+({double})\s+({double})\s+({double}).+\n"
                 r"\s+({double})\s+({double})\s+({double}).+\n"
                 r"\s+({double})\s+({double})\s+({double})".format(double=GENERAL_REGEX.double_number)
    },
    "basis_vectors": {
        "regex": r'\s+({double})\s+({double})\s+({double})\s+{double}\s+{double}\s+{double}'.format(
            double=GENERAL_REGEX.double_number)
    },
    "pressure": {
        "regex": r"external pressure\s+=\s+({0})\s+kB".format(GENERAL_REGEX.double_number),
        "occurrences": -1,
        "output_type": "float",
    },
    "total_force": {
        "regex": r"total drift:\s+({0})\s+({0})\s+({0})".format(GENERAL_REGEX.double_number),
        "occurrences": -1,
        "output_type": "float",
        "match_groups": [1, 2, 3]
    },
    "zero_point_energy": {
        "regex": r"f\s\s=.*2PiTHz\s+\d+\.\d+\s+cm\-1\s+({0})\s+meV".format(GENERAL_REGEX.double_number),
        "start_flag": "Eigenvectors and eigenvalues of the dynamical matrix",
        "output_type": "float",
    }
}

TOTAL_ENERGY_CONTRIBUTIONS = {
    "hartree": {
        "regex": _COMMON_REGEX.format("Hartree", GENERAL_REGEX.double_number),
        "occurrences": -1,
        "output_type": "float",
        "match_groups": [1, 2, 3, 4, 5, 6]
    },
    "ewald": {
        "regex": _COMMON_REGEX.format("Ewald", GENERAL_REGEX.double_number),
        "occurrences": -1,
        "output_type": "float",
        "match_groups": [1, 2, 3, 4, 5, 6]
    },
    "exchange_correlation": {
        "regex": _COMMON_REGEX.format("E\(xc\)", GENERAL_REGEX.double_number),
        "occurrences": -1,
        "output_type": "float",
        "match_groups": [1, 2, 3, 4, 5, 6]
    }
}
