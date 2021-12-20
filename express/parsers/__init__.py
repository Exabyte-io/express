import os

from typing import Tuple


class BaseParser(object):
    """
    Base Parser class.
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def get_unix_path_names(self, full_path: str) -> Tuple[str, str]:
        """
        Return unix-like dirname and basename from a full path
        """
        *dirname, basename = os.path.split(full_path)
        return os.sep.join(dirname), basename

    def _get_file_content(self, file_path):
        """
        Returns the content of a given file.

        Args:
            file_path (str): file path.

        Returns:
             str
        """
        content = ""
        if file_path and os.path.exists(file_path):
            with open(file_path) as f:
                content = f.read()
        return content
