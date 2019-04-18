from express.parsers.settings import GENERAL_REGEX

PDOS_TOT_FILE = "pdos_tot"
XML_DATA_FILE = "data-file.xml"
NEB_DAT_FILE = "__prefix__.dat"
PHONON_DOS_FILE = "phonon_dos.out"
PHONON_MODES_FILE = "normal_modes.out"

COMMON_REGEX = r"{0}\s+[=:<>]\s*([-+]?\d*\.?\d*([Ee][+-]?\d+)?)"
DOUBLE_REGEX = GENERAL_REGEX.double_number

STERNHEIMER_GW0_DIR_PATTERN = "/_gw0/"
STERNHEIMER_GW_TITLE = "SternheimerGW"

REGEX = {
    "total_energy": {
        "regex": COMMON_REGEX.format("total energy"),
        "start_flag": "!",
        "occurrences": -1,
        "output_type": "float"
    },
    "pdos_file": {
        "regex": r'.*\.pdos_atm#(?P<atom_num>\d+)\((?P<atom_name>\w+)\)'
                 r'_wfc#(?P<orbit_num>\d+)\((?P<orbit_symbol>\w)\)',
    },
    "convergence_electronic": {
        "regex": r"estimated scf accuracy\s+<\s+({0})".format(DOUBLE_REGEX),
        "output_type": "float",
    },
    "convergence_ionic_blocks": {
        "regex": r"\s+Self-consistent Calculation.+?\n(.+?)\s+convergence has been achieved"
    },
    "convergence_ionic_energies": {
        "regex": r"total energy\s+=\s+({0})".format(DOUBLE_REGEX),
        "output_type": "float",
    },
    "bfgs_block": {
        "regex": r"new unit-cell volume.+?Writing output data file",
    },
    "lattice": {
        "regex": (
            r"CELL_PARAMETERS\s+\(angstrom\)"
            r"\s+({0})\s+({0})\s+({0})"
            r"\s+({0})\s+({0})\s+({0})"
            r"\s+({0})\s+({0})\s+({0})"
        ).format(DOUBLE_REGEX)
    },
    "lattice_alat": {
        "regex": (
            r"crystal axes:.*\n"
            r".*(\s+{0})\s+({0})\s+({0}\s+).*\n"
            r".*(\s+{0})\s+({0})\s+({0}\s+).*\n"
            r".*(\s+{0})\s+({0})\s+({0}\s+).*\n"
        ).format(DOUBLE_REGEX)
    },
    "lattice_parameter_alat": {
        "regex": r"lattice parameter \(alat\)\s+=\s+({0})\s+".format(DOUBLE_REGEX),
        "output_type": "float",
    },
    "number_of_atoms": {
        "regex": r"number of atoms/cell\s+=\s+(\d+)",
        "output_type": "int",
    },
    "basis_alat": lambda number_of_atoms: {
        "regex": r".+?\d\s+([A-Z][a-z]?).+?({0})\s+({0})\s+({0}).+?\n".format(DOUBLE_REGEX),
        "start_flag": "positions (alat units)",
        "occurrences": number_of_atoms,
        "output_type": "str",
        "match_groups": [1, 2, 3, 4]
    },
    "ion_position": {
        "regex": r"([A-Z][a-z]?)\s+({0})\s+({0})\s+({0})".format(DOUBLE_REGEX)
    },
    "stress_tensor": {
        "regex": r"^\s*{0}\s+{0}\s+{0} +({0})\s+({0})\s+({0})".format(DOUBLE_REGEX),
        "start_flag": "Forces acting on atoms",
        "occurrences": 3,
        "output_type": "float",
        "match_groups": [1, 2, 3]
    },
    "pressure": {
        "regex": r"\s*total\s+stress\s+\(Ry/bohr\*\*3\)\s*\(kbar\)\s*P=\s*({0})".format(DOUBLE_REGEX),
        "start_flag": "Forces acting on atoms",
        "occurrences": -1,
        "output_type": "float"
    },
    "total_force": {
        "regex": COMMON_REGEX.format("Total force"),
        "start_flag": "Total force",
        "occurrences": -1,
        "output_type": "float"
    },
    "forces_on_atoms": {
        "regex": r"^\s*atom\s+\d+\s+type\s+\d+\s+force\s+=\s+({0})\s+({0})\s+({0})".format(DOUBLE_REGEX),
        "start_flag": "Forces acting on atoms",
        "occurrences": 0,
        "output_type": "float",
        "match_groups": [1, 2, 3]
    },
    "zero_point_energy": {
        "regex": r"freq\s\(\s+\d+\)\s+\=\s+\d+\.\d+\s+\[THz\]\s+\=\s+({0})\s+\[cm\-1\]".format(DOUBLE_REGEX),
        "start_flag": "Diagonalizing the dynamical matrix",
        "output_type": "float"
    },
    'phonon_frequencies': {
        "regex": r'freq\s\(\s+\d+\)\s+\=\s+-*\d+\.\d+\s+\[THz\]\s+\=\s+({})\s+\[cm\-1\]'.format(DOUBLE_REGEX)
    },
    'qpoints': {
        "regex": r'q\s+\=\s+({0})\s+({0})\s+({0})'.format(DOUBLE_REGEX)
    },
    "reaction_coordinates": {
        "regex": r"^\s+({0})\s+{0}\s+{0}".format(DOUBLE_REGEX),
        "output_type": "float",
    },
    "reaction_energies": {
        "regex": r"^\s+{0}\s+({0})\s+{0}".format(DOUBLE_REGEX),
        "output_type": "float",
    },
    "potential_profile": {
        "regex": r"^\s+({0})\s+{0}\s+({0})\s+({0})\s+({0})".format(DOUBLE_REGEX),
        "occurrences": 0,
        "output_type": "float",
        "match_groups": [1, 2, 3, 4]
    },
    "charge_density_profile": {
        "regex": r"^\s+({0})\s+({0})\s+{0}\s+{0}\s+{0}".format(DOUBLE_REGEX),
        "occurrences": 0,
        "output_type": "float",
        "match_groups": [1, 2]
    },
    "sternheimer_gw_kpoint": {
        "regex": r"^\s+GWKpoint cart :\s+({0})\s+({0})\s+({0})".format(DOUBLE_REGEX),
        "occurrences": 0,
        "output_type": "float",
        "match_groups": [1, 2, 3]
    },
    "sternheimer_gw_eigenvalues": {
        "regex": r"^\s+GW qp energy \(eV\)(.*)",
        "occurrences": 0,
        "output_type": "str",
    },
}

TOTAL_ENERGY_CONTRIBUTIONS = {
    "harris_foulkes": {
        "regex": COMMON_REGEX.format("Harris-Foulkes estimate"),
        "start_flag": "!",
        "occurrences": -1,
        "output_type": "float"
    },
    "one_electron": {
        "regex": COMMON_REGEX.format("one-electron contribution"),
        "start_flag": "!",
        "occurrences": -1,
        "output_type": "float"
    },
    "hartree": {
        "regex": COMMON_REGEX.format("hartree contribution"),
        "start_flag": "!",
        "occurrences": -1,
        "output_type": "float"
    },
    "exchange_correlation": {
        "regex": COMMON_REGEX.format("xc contribution"),
        "start_flag": "!",
        "occurrences": -1,
        "output_type": "float"
    },
    "ewald": {
        "regex": COMMON_REGEX.format("ewald contribution"),
        "start_flag": "!",
        "occurrences": -1,
        "output_type": "float"
    },
    "smearing": {
        "regex": COMMON_REGEX.format("smearing contrib\.\s+\(-TS\)"),
        "start_flag": "!",
        "occurrences": -1,
        "output_type": "float"
    }
}
