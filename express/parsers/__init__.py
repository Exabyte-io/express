import os

from express.mixins import RoundNumericValuesMixin


class BaseParser(RoundNumericValuesMixin):
    """
    Base Parser class.
    """

    # Whether the structures this parser extracts are molecules rather than crystals. Read by
    # `express.properties.material.Material`, which still uses getattr because it is also
    # constructed with parser=None.
    is_non_periodic = False

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.version = kwargs.get("version", None)

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
