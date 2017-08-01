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
        if eigenvalue['spin'] == spin_map[spin_index]:
            return eigenvalue['energies']
