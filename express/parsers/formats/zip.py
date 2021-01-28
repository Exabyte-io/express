from __future__ import absolute_import

import os
import zipfile


class BaseZipParser(object):
    """
    Base Zip parser class.
    """

    def __init__(self, zip_file_path):
        self.zip_path = zip_file_path
        self.zip_dir_name = None
        self.zip_file = None
        if self.zip_path and os.path.exists(self.zip_path):
            try:
                self.zip_dir_name = os.path.dirname(self.zip_path)
                self.zip_file = zipfile.ZipFile(self.zip_path)
            except Exception as error:
                print(f"Failed to parse {self.zip_path}: {error!s}")
