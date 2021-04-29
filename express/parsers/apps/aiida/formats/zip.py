import json
from zipfile import ZipFile
from zipfile import BadZipFile

import esse

from express.parsers.apps.aiida.settings import SUPPORTED_AIIDA_ARCHIVE_VERSION
from express.parsers.apps.aiida.settings import SUPPORTED_AIIDA_VERSION
from express.parsers.apps.aiida.settings import TEMPLATES_MATERIALS_PATH


ES = esse.ESSE()
SCHEMA_MATERIAL = ES.get_schema_by_id('material')


__all__ = [
    'AiidaArchivefileParseError',
    'AiidaZipParser',
    'BadAiidaArchiveZipFile',
    'BadZipFile',
]


class BadAiidaArchiveZipFile(ValueError):
    """Error raised when parsing of archive file critically failed.

    May indicate that the file may not actually be an
    AiiDA archive file.
    """

    def __init__(self, path, error):
        self.path = path
        self.error = error


class AiidaArchiveFileParseError(RuntimeError):
    """Error raised when error occurred during parsing of archive file.
    """

    def __init__(self, path, reason):
        self.path = path
        self.reason = reason


class AiidaZipParser:
    """
    Parser for AiiDA archive zip files.

    Args:
        zip_file_path: path to AiiDA archive file

    Raises:
        BadZipFile:
            The file at the given path cannot be read as a valid zip file.
        BadAiidaArchiveZipFile:
            The file at the give path cannot be read as valid AiiDA archive file.
    """

    def __init__(self, zip_file_path):
        self.zip_file_path = zip_file_path

        self._metadata = None
        self._data = None

        self._check_supported_versions()  # triggers parsing of metadata

    @property
    def metadata(self):
        if self._metadata is None:
            with ZipFile(self.zip_file_path) as source:
                self._metadata = json.loads(source.read('metadata.json'))
        return self._metadata

    @property
    def data(self):
        if self._data is None:
            with ZipFile(self.zip_file_path) as source:
                self._data = json.loads(source.read('data.json'))
        return self._data

    def _check_supported_versions(self):
        """
        Check whether the versions of the exported archive file are supported.

        Raises:
            RuntimeError
        """
        try:
            aiida_version = self.metadata['aiida_version']
            export_version = self.metadata['export_version']
        except KeyError as error:
            raise BadAiidaArchiveZipFile(self.zip_file_path, error)

        if self.metadata['aiida_version'] != SUPPORTED_AIIDA_VERSION:
            raise AiidaArchiveFileParseError(
                path=self.zip_file_path,
                reason=f"aiida_version ({self.metadata['aiida_version']}) not supported. "
                f"Supported: {SUPPORTED_AIIDA_VERSION}")

        if self.metadata['export_version'] != SUPPORTED_AIIDA_ARCHIVE_VERSION:
            raise AiidaArchiveFileParseError(
                path=self.zip_file_path,
                reason=f"archive export_version ({self.metadata['export_version']}) not supported. "
                f"Supported: {SUPPORTED_AIIDA_ARCHIVE_VERSION}")

    def structures(self):
        """
        Extract all structures from compatible AiiDA archive zip files.

        Returns:
            list
        """

        return list(self._gather_structures(self.data))

    @classmethod
    def _gather_structures(cls, data):
        """
        Yield parsed structure objects from nodes within AiiDA archive.

        Args:
            data (dict): deserialized data.json object
        Yields:
            dict
        """

        nodes = data['export_data']['Node']
        structure_nodes = {pk: node for (pk, node) in nodes.items()
                           if node['node_type'] == 'data.structure.StructureData.'}

        for pk in structure_nodes:
            export_data = data['export_data']['Node'][pk]
            node_attributes = data['node_attributes'][pk]
            yield cls._parse_structure_node_attributes(export_data, node_attributes)

    @staticmethod
    def _parse_structure_node_attributes(export_data, attributes):
        """
        Parse an AiiDA StructureData node.
        """

        # Prepare mapping
        assert export_data['node_type'] == 'data.structure.StructureData.'

        sites = list(enumerate(attributes['sites']))
        kinds = {kind['name']: kind for kind in attributes['kinds']}
        assert all(len(kind['symbols']) == 1 for kind in kinds.values())

        instance = json.loads(TEMPLATES_MATERIALS_PATH.read_text())
        instance.update({
            '_id': export_data['uuid'],
            'created_at': export_data['ctime'],
            'lattice': {
                'vectors': {
                    'a': attributes['cell'][0],
                    'b': attributes['cell'][1],
                    'c': attributes['cell'][2],
                }
            },
            'basis': {
                'elements': [{'id': _id, 'value': kinds[site['kind_name']]['name']} for _id, site in sites],
                'coordinates': [{'id': _id, 'value': site['position']} for _id, site in sites],
            }
        })

        # Validate result and return
        ES.validate(instance, schema=SCHEMA_MATERIAL)
        return instance
