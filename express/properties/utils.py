from mat3ra.made.tools.convert.utils import calculate_padded_cell_simple_cubic
from mat3ra.made.utils import get_center_of_coordinates


def eigenvalues(eigenvalues_at_kpoints, kpoint_index=0, spin_index=0):
    """
    Returns eigenvalues for a given kpoint and spin.

    Args:
        eigenvalues_at_kpoints (list): a list of eigenvalues for all kpoints.
        kpoint_index (int): kpoint index.
        spin_index (int): spin index.

    Returns:
         ndarray
    """
    spin_map = {0: 0.5, 1: -0.5}
    for eigenvalue in eigenvalues_at_kpoints[kpoint_index]["eigenvalues"]:
        if eigenvalue["spin"] == spin_map[spin_index]:
            return eigenvalue["energies"]


def to_array_with_ids(array):
    """
    Converts a given array to an array of objects with id.

    Args:
        array (list): array to convert

    Returns:
        list
    """
    return [{"id": index, "value": value} for index, value in enumerate(array)]


def box_molecule(selected_basis, parsed_bases):
    """
    Returns lattice vectors and the selected basis centered in them: made's simple-cubic padding,
    sized to hold every basis in `parsed_bases` so an optimization moves atoms inside a fixed box
    rather than resizing it. Printed coordinates straddle the origin, and atoms left outside the box
    read as extra fragments and corrupt the InChI.
    """
    coordinates = [coordinate["value"] for coordinate in selected_basis["coordinates"]]
    cells = [
        calculate_padded_cell_simple_cubic([point["value"] for point in other["coordinates"]]) for other in parsed_bases
    ]
    edge = max(vectors[0][0] for vectors in cells)
    center = get_center_of_coordinates(coordinates)
    centered = [[x - center[axis] + edge / 2 for axis, x in enumerate(coordinate)] for coordinate in coordinates]
    return (
        {"vectors": {"a": [edge, 0.0, 0.0], "b": [0.0, edge, 0.0], "c": [0.0, 0.0, edge], "alat": 1}},
        dict(selected_basis, coordinates=to_array_with_ids(centered)),
    )
