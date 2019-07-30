import os


def find_file(name, path):
    """
    Finds file with the specified name in the given path.

    Args:
        name (str): file name.
        path (str): starting path for search.

    Returns:
        str: absolute file path (if found)
    """
    for root, dirs, files in os.walk(path, followlinks=True):
        for file in files:
            if name in file:
                return os.path.join(root, file)


def find_fines_by_name_substring(name, path):
    matches = []
    for root, dirs, files in os.walk(path, followlinks=True):
        for file_ in files:
            if name in file_:
                matches.append(os.path.join(root, file_))
    return matches


def get_element_counts(basis):
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
            element_counts.append({
                "count": 1,
                "value": element["value"]
            })
        previous_element = basis["elements"][index]
    return element_counts


def lattice_basis_to_poscar(lattice, basis, basis_units="cartesian"):
    element_counts = get_element_counts(basis)
    return "\n".join([
        "material",
        "1.0",
        "\t".join(["{0:14.9f}".format(x) for x in lattice["vectors"]["a"]]),
        "\t".join(["{0:14.9f}".format(x) for x in lattice["vectors"]["b"]]),
        "\t".join(["{0:14.9f}".format(x) for x in lattice["vectors"]["c"]]),
        " ".join((e["value"] for e in element_counts)),
        " ".join((str(e["count"]) for e in element_counts)),
        basis_units,
        "\n".join([" ".join(["{0:14.9f}".format(v) for v in x["value"]]) for x in basis["coordinates"]])
    ])
