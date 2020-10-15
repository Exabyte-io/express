from express.parsers import BaseParser
from express.parsers.apps.aiida.formats.zip import AiidaZipParser

from express.parsers.utils import find_files_by_name_substring


class AiidaArchiveParser(BaseParser):

    def __init__(self, *args, **kwargs):
        super(AiidaArchiveParser, self).__init__(*args, **kwargs)
        self.path = self.kwargs["workDir"]

    def find_zip_files(self):
        if self.path is not None:
            for zip_file_path in find_files_by_name_substring('.zip', self.path):
                yield zip_file_path

    def structures(self):
        self.zip_parser = AiidaZipParser(self.path)
        structures = []
        for zip_file in self.find_zip_files():
            zip_parser = AiidaZipParser(zip_file)
            structures.extend(zip_parser.structures())
        return structures
