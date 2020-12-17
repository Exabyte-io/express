import esse

from express.parsers.formats.zip import BaseZipParser
from express.parsers.formats.jsonfile import BaseJSONParser
from express.parsers.apps.aiida.settings import SUPPORTED_AIIDA_ARCHIVE_VERSION, SUPPORTED_AIIDA_VERSION


ES = esse.ESSE()
SCHEMA_MATERIAL = ES.get_schema_by_id('material')


class AiidaZipParser(BaseZipParser):

    def __init__(self, *args, **kwargs):
        self.json_parser = BaseJSONParser
        super(AiidaZipParser, self).__init__(*args, **kwargs)

    def structures(self):
        structures = []

        with self.zip_file as source:
            metadata = self.json_parser.loads(source.read('metadata.json'))
            data = self.json_parser.loads(source.read('data.json'))

            # version check
            assert metadata['aiida_version'] == SUPPORTED_AIIDA_VERSION
            assert metadata['export_version'] == SUPPORTED_AIIDA_ARCHIVE_VERSION

            # gather structure nodes
            nodes = data['export_data']['Node']
            structure_nodes = {pk: node for (pk, node) in nodes.items()
                               if node['node_type'] == 'data.structure.StructureData.'}

            for pk in structure_nodes:
                export_data = data['export_data']['Node'][pk]
                node_attributes = data['node_attributes'][pk]
                structures.append(self._parse_structure_node_attributes(export_data, node_attributes))

        return structures

    @staticmethod
    def _parse_structure_node_attributes(export_data, attributes):
        """Parse an AiiDA StructureData node."""
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
