import math
from typing import List

from mat3ra.esse.models.properties_directory.structural.lattice import LatticeSchema
from mat3ra.made.cell.primitive_cell import get_primitive_lattice_vectors_from_config
from mat3ra.utils.constants import COEFFICIENTS
from mat3ra.utils.string import remove_comments_from_source_code
from mat3ra.parsers.applications.espresso.pw_x.stdin.parser import EspressoPwxStdinParser

# Maps QE ibrav codes → made/esse Bravais type strings
IBRAV_TO_LATTICE_TYPE = {
    1:  "CUB",
    2:  "FCC",
    3:  "BCC",  -3: "BCC",
    4:  "HEX",
    5:  "RHL",  -5: "RHL",
    6:  "TET",
    7:  "BCT",
    8:  "ORC",
    9:  "ORCC", -9: "ORCC",
    10: "ORCF",
    11: "ORCI",
    12: "MCL",  -12: "MCL",
    13: "MCLC",
    14: "TRI",
}


def _get_cell_from_ibrav(system: dict) -> List[List[float]]:
    ibrav = int(system.get("ibrav", 0))
    lattice_type = IBRAV_TO_LATTICE_TYPE.get(ibrav)
    if lattice_type is None:
        raise ValueError(f"Unsupported ibrav={ibrav}")

    has_celldm = "celldm1" in system

    if has_celldm:
        a = float(system["celldm1"]) * COEFFICIENTS["BOHR_TO_ANGSTROM"]
        b = a * float(system.get("celldm2", 1))
        c = a * float(system.get("celldm3", 1))
        # celldm(4,5,6) are cosines → convert to degrees
        alpha = math.degrees(math.acos(float(system.get("celldm4", 0))))
        beta  = math.degrees(math.acos(float(system.get("celldm5", 0))))
        gamma = math.degrees(math.acos(float(system.get("celldm6", 0))))
    else:
        a = float(system.get("a", 1))
        b = float(system.get("b", a))
        c = float(system.get("c", a))
        alpha = math.degrees(math.acos(float(system["cosbc"]))) if "cosbc" in system else float(system.get("alpha", 90))
        beta  = math.degrees(math.acos(float(system["cosac"]))) if "cosac" in system else float(system.get("beta",  90))
        gamma = math.degrees(math.acos(float(system["cosab"]))) if "cosab" in system else float(system.get("gamma", 90))

    lattice_config = LatticeSchema(type=lattice_type, a=a, b=b, c=c, alpha=alpha, beta=beta, gamma=gamma)

    return get_primitive_lattice_vectors_from_config(lattice_config)


class PwInputFile:
    def __init__(self, input_text: str):
        text = remove_comments_from_source_code(input_text, language="fortran")
        parser = EspressoPwxStdinParser(text)

        system = parser.get_namelist("SYSTEM")
        ibrav = int(system.get("ibrav", 0))

        celldm1_angstrom = float(system["celldm1"]) * COEFFICIENTS["BOHR_TO_ANGSTROM"] if "celldm1" in system else None

        # Delegate crystal lattice calculation based on ibrav value
        cell = parser.get_card_cell_parameters(celldm1_angstrom) if ibrav == 0 else _get_cell_from_ibrav(system)

        atom_names, positions = parser.get_card_atomic_positions(cell, celldm1_angstrom)

        self.structure = {
            "cell": cell,
            "atom_names": atom_names,
            "positions": positions,
        }
