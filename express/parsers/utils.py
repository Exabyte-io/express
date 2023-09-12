import os
import re
from typing import Optional, List
from pathlib import Path


def find_file(name: str, path: str) -> Optional[str]:
    """
    Finds file with the specified name in the given path.

    Args:
        name (str): file name or absolute path
        path (str): starting path for search.

    Returns:
        str: absolute file path (if found)
    """
    basename = os.path.basename(name)
    for root, _, files in os.walk(path, followlinks=True):
        for file in files:
            if basename in file:
                return os.path.join(root, file)


def find_files_by_name_substring(name: str, path: str) -> List[str]:
    matches = []
    for root, _, files in os.walk(path, followlinks=True):
        for file_ in files:
            if name in file_:
                matches.append(os.path.join(root, file_))
    return matches


def find_files_by_regex(regex: str, path: Path) -> List[Path]:
    """Find files using a regular expression for the filename.

    This function walks through subdirectories and matches filenames (not absolute path)
    against a regular expression.

    Returns:
        A list of Path objects with filenames matching the provided regular expression.
    """
    pattern = re.compile(regex)
    matches = []
    for p in path.rglob("*"):
        if p.is_file() and pattern.match(p.name):
            matches.append(p.resolve())
    return matches


def get_element_counts(basis: dict) -> List[dict]:
    """
    Returns chemical elements with their count wrt their original order in the basis.
    Note: entries for the same element separated by another element are considered separately.
    [{"count":1, "value":"Zr"}, {"count":23, "value":"H"}, {"count":11, "value":"Zr"}, {"count":1, "value":"H"}]
    """
    element_counts = []
    previous_element = None
    for index, element in enumerate(basis["elements"]):
        if previous_element and previous_element["value"] == element["value"]:
            element_counts[-1]["count"] += 1
        else:
            element_counts.append({"count": 1, "value": element["value"]})
        previous_element = basis["elements"][index]
    return element_counts


def lattice_basis_to_poscar(lattice: dict, basis: dict, basis_units: str = "cartesian") -> str:
    element_counts = get_element_counts(basis)
    return "\n".join(
        [
            "material",
            "1.0",
            "\t".join(["{0:14.9f}".format(x) for x in lattice["vectors"]["a"]]),
            "\t".join(["{0:14.9f}".format(x) for x in lattice["vectors"]["b"]]),
            "\t".join(["{0:14.9f}".format(x) for x in lattice["vectors"]["c"]]),
            " ".join((e["value"] for e in element_counts)),
            " ".join((str(e["count"]) for e in element_counts)),
            basis_units,
            "\n".join([" ".join(["{0:14.9f}".format(v) for v in x["value"]]) for x in basis["coordinates"]]),
        ]
    )
