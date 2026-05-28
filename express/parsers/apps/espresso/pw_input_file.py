import math
import re
from typing import List, Optional, Tuple

from mat3ra.esse.models.properties_directory.structural.lattice import LatticeSchema
from mat3ra.made.cell.primitive_cell import get_primitive_lattice_vectors_from_config

BOHR_TO_ANGSTROM = 0.529177210903

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


def _strip_comments(text: str) -> str:
    text = re.sub(r"!.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"#.*$", "", text, flags=re.MULTILINE)
    return text


def _parse_namelist(text: str, name: str) -> dict:
    """Extract key=value pairs from a Fortran namelist block &NAME ... /"""
    match = re.search(rf"&{name}\s*([\s\S]*?)\/", text, re.IGNORECASE)
    if not match:
        return {}
    block = match.group(1)
    result = {}
    # Regular key=value pairs
    for k, v in re.findall(r"(\w+)\s*=\s*([^,\n/=]+)", block):
        result[k.strip().lower()] = v.strip()
    # celldm(N) with explicit index
    for n, v in re.findall(r"celldm\s*\(\s*(\d+)\s*\)\s*=\s*([^,\n/]+)", block, re.IGNORECASE):
        result[f"celldm{n}"] = v.strip()
    return result


def _get_cell_from_ibrav(system: dict) -> List[List[float]]:
    ibrav = int(system.get("ibrav", 0))
    lattice_type = IBRAV_TO_LATTICE_TYPE.get(ibrav)
    if lattice_type is None:
        raise ValueError(f"Unsupported ibrav={ibrav}")

    has_celldm = "celldm1" in system

    if has_celldm:
        a = float(system["celldm1"]) * BOHR_TO_ANGSTROM
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


def _parse_cell_parameters(text: str, celldm1_angstrom: Optional[float]) -> List[List[float]]:
    match = re.search(
        r"CELL_PARAMETERS\s*[{(]?\s*(\w+)\s*[)}]?\s*\n"
        r"((?:[ \t]*[-\d.eEdD+]+[ \t]+[-\d.eEdD+]+[ \t]+[-\d.eEdD+]+[ \t]*\n?){3})",
        text, re.IGNORECASE,
    )
    if not match:
        raise ValueError("CELL_PARAMETERS card not found")
    units = match.group(1).lower()
    rows = [list(map(float, line.split())) for line in match.group(2).strip().splitlines()]
    if units == "bohr":
        rows = [[v * BOHR_TO_ANGSTROM for v in row] for row in rows]
    elif units == "alat":
        if not celldm1_angstrom:
            raise ValueError("alat units require celldm(1)")
        rows = [[v * celldm1_angstrom for v in row] for row in rows]
    return rows  # angstrom: use as-is


def _parse_atomic_positions(
    text: str, cell: List[List[float]], celldm1_angstrom: Optional[float]
) -> Tuple[List[str], List[List[float]]]:
    match = re.search(
        r"ATOMIC_POSITIONS\s*[{(]?\s*(\w+)\s*[)}]?\s*\n"
        r"((?:[ \t]*\w+[ \t]+[-\d.eEdD+]+[ \t]+[-\d.eEdD+]+[ \t]+[-\d.eEdD+]+.*\n?)+)",
        text, re.IGNORECASE,
    )
    if not match:
        raise ValueError("ATOMIC_POSITIONS card not found")
    units = match.group(1).lower()
    names, positions = [], []
    for line in match.group(2).strip().splitlines():
        parts = line.split()
        if len(parts) < 4:
            continue
        symbol = parts[0]
        coords = list(map(float, parts[1:4]))
        if units == "crystal":
            # fractional → Cartesian: coords_cart[j] = sum_i frac[i] * cell[i][j]
            coords = [
                sum(coords[i] * cell[i][j] for i in range(3))
                for j in range(3)
            ]
        elif units == "bohr":
            coords = [v * BOHR_TO_ANGSTROM for v in coords]
        elif units == "alat":
            if not celldm1_angstrom:
                raise ValueError("alat units require celldm(1)")
            coords = [v * celldm1_angstrom for v in coords]
        names.append(symbol)
        positions.append(coords)
    return names, positions


class PwInputFile:
    """
    QE pw.x input parser.
    Uses get_primitive_lattice_vectors_from_config() from mat3ra.made for ibrav != 0.

    self.structure dict keys match qe-tools PwInputFile.structure:
        cell        - 3x3 list of lists (Angstrom)
        atom_names  - list of element symbols
        positions   - list of Cartesian coords (Angstrom)
    """

    def __init__(self, input_text: str):
        text = _strip_comments(input_text)
        system = _parse_namelist(text, "SYSTEM")
        ibrav = int(system.get("ibrav", 0))

        celldm1_angstrom = (
            float(system["celldm1"]) * BOHR_TO_ANGSTROM if "celldm1" in system else None
        )

        cell = (
            _parse_cell_parameters(text, celldm1_angstrom)
            if ibrav == 0
            else _get_cell_from_ibrav(system)   # ← delegates to made
        )

        atom_names, positions = _parse_atomic_positions(text, cell, celldm1_angstrom)

        self.structure = {
            "cell": cell,
            "atom_names": atom_names,
            "positions": positions,
        }
