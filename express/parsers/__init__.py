import os


class BaseParser(object):
    """
    Base Parser class.
    """

    # TODO: This looks dangerous
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    @property
    def full_stdout_file_path(self):
        return os.path.join(
            self.kwargs.get("work_dir", ""),
            self.kwargs.get("stdout_file", "")
        )

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
