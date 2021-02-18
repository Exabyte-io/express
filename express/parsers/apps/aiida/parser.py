from express.parsers import BaseParser
from express.parsers.apps.aiida.formats.zip import AiidaArchiveFileParseError
from express.parsers.apps.aiida.formats.zip import AiidaZipParser
from express.parsers.apps.aiida.formats.zip import BadAiidaArchiveZipFile
from express.parsers.apps.aiida.formats.zip import BadZipFile
from express.parsers.utils import lattice_basis_to_poscar

from express.parsers.utils import find_files_by_name_substring


class AiidaArchiveParser(BaseParser):

    def __init__(self, *args, **kwargs):
        """
        AiiDA archive (zip) file parser.
        """

        super(AiidaArchiveParser, self).__init__(*args, **kwargs)
        self.path = self.kwargs["work_dir"]

    def find_zip_files(self):
        """
        Find all zip-files in path.

        Yields:
            str
        """

        if self.path is not None:
            for zip_file_path in find_files_by_name_substring('.zip', self.path):
                yield zip_file_path

    def initial_structure_strings(self):
        """
        Extract all structures from AiiDA archive (zip) files in path.

        Returns:
            list
        """

        structures = []
        for zip_file_path in self.find_zip_files():
            try:
                zip_parser = AiidaZipParser(zip_file_path)
            except BadZipFile as error:
                print(f"Unable to open zip-file '{zip_file_path}': {error}")
            except BadAiidaArchiveZipFile:
                continue  # assume this zip-file is not actually an AiiDA archive file
            except AiidaArchiveFileParseError as error:
                print(f"Failed to read AiiDA archive zip-file '{error.path}': {error.reason}")
            else:
                for structure in zip_parser.structures():
                    lattice = structure['lattice']
                    basis = structure['basis']
                    structures.append(lattice_basis_to_poscar(lattice, basis))
        return structures

    # TODO: This is probably not how we want to handle this.
    final_structure_strings = initial_structure_strings
