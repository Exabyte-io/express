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


def box_molecule(basis, bases):
    """
    Puts a molecule into the cell its application does not print: made's simple-cubic padding
    convention, the same one that gives every non-periodic material on the platform its box.

    One cell for every basis in `bases`, so the structures of one calculation stay comparable: an
    optimization moves atoms inside a fixed box rather than resizing it. Sized to whichever geometry
    needs the most room, and the basis is then centered in it -- printed coordinates straddle the
    origin, and atoms outside the box read as extra fragments and corrupt the InChI.

    Args:
        basis (dict): the basis to center.
        bases (list): every basis the cell has to hold.

    Returns:
        tuple[dict, dict]: lattice vectors and the centered basis.
    """
    coordinates = [coordinate["value"] for coordinate in basis["coordinates"]]
    edge = max(
        calculate_padded_cell_simple_cubic([point["value"] for point in other["coordinates"]])[0][0] for other in bases
    )
    center = get_center_of_coordinates(coordinates)
    centered = [[x - center[axis] + edge / 2 for axis, x in enumerate(coordinate)] for coordinate in coordinates]
    return (
        {"vectors": {"a": [edge, 0.0, 0.0], "b": [0.0, edge, 0.0], "c": [0.0, 0.0, edge], "alat": 1}},
        dict(basis, coordinates=to_array_with_ids(centered)),
    )
