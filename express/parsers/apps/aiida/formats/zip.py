import zipfile

import esse

from express.parsers.formats.jsonfile import BaseJSONParser
from express.parsers.apps.aiida.settings import SUPPORTED_AIIDA_ARCHIVE_VERSION, SUPPORTED_AIIDA_VERSION


ES = esse.ESSE()
SCHEMA_MATERIAL = ES.get_schema_by_id('material')


class AiidaZipParser:
    """
    Parser for AiiDA archive zip files.
    """

    def __init__(self, zip_file_path):
        self.zip_file = zipfile.ZipFile(zip_file_path)

        self.json_parser = BaseJSONParser

    def structures(self):
        """
        Extract all structures from compatible AiiDA archive zip files.

        Returns:
            list
        """

        with self.zip_file as source:

            # check that versions are supported (raises RuntimeError)
            metadata = self.json_parser.loads(source.read('metadata.json'))
            self._check_supported_versions(metadata)

            # gather structure nodes into list and return
            data = self.json_parser.loads(source.read('data.json'))
            return list(self._gather_structures(data))

    def _check_supported_versions(self, metadata):
        """
        Check whether the versions of the exported archive file are supported.

        Args:
            metadata (dict): deserialized metadata.json object

        Raises:
            RuntimeError
        """
        if metadata['aiida_version'] != SUPPORTED_AIIDA_VERSION:
            raise RuntimeError(
                f"aiida_version ({metadata['aiida_version']}) not supported. "
                f"Supported: {SUPPORTED_AIIDA_VERSION}")

        if metadata['export_version'] != SUPPORTED_AIIDA_ARCHIVE_VERSION:
            raise RuntimeError(
                f"archive export_version ({metadata['export_version']}) not supported. "
                f"Supported: {SUPPORTED_AIIDA_ARCHIVE_VERSION}")


    def _gather_structures(self, data):
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
            yield self._parse_structure_node_attributes(export_data, node_attributes)

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

        instance = {
            'schemaVersion':  '0.2.0',

            # TODO: THE FOLLOWING VARIABLES ARE PLACEHOLDERS!
            '_id': export_data['uuid'],
            'exabyteId': 'PLACEHOLDER',
            'hash': 'PLACEHOLDER',

            # TODO: Gather from export data?
            'creator': 'CREATOR',
            'owner': 'OWNER',

            # THE FOLLOWING ATTRIBUTES SHOULD BE IMPROVED:
            'created_at': export_data['ctime'],  # TODO: or maybe mtime?

            # Actual materials-related data
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
            },
        }

        # Validate result and return
        ES.validate(instance, schema=SCHEMA_MATERIAL)
        return instance
