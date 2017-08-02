import os


class BaseParser(object):
    """
    Base Parser class.

    Args:
        work_dir (str): working directory path.
        stdout_file (str): path to the stdout file.
    """

    def __init__(self, work_dir, stdout_file=None):
        self.work_dir = work_dir
        self.stdout_file = stdout_file

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

    def _get_stdout_content(self):
        """
        Returns the content of stdout file.

        Returns:
             str
        """
        return self._get_file_content(self.stdout_file)
