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
