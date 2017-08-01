class BaseParser(object):
    """
    Base Parser class.

    Args:
        work_dir (str): working directory path.
        kwargs (dict):
            app_stdout (str): path to the application stdout file.
    """

    def __init__(self, work_dir, **kwargs):
        self.work_dir = work_dir
        self.kwargs = kwargs

    def _get_file_content(self, file_path):
        """
        Returns the content of a given file.

        Args:
            file_path (str): file path.

        Returns:
             str
        """
        with open(file_path) as f:
            return f.read()

    def _get_stdout_content(self):
        """
        Returns the content of stdout file.

        Returns:
             str
        """
        return self._get_file_content(self.kwargs["app_stdout"])
