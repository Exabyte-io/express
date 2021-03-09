import os
from typing import Dict

from . import NonScalarProperty


class FileContent(NonScalarProperty):
    """
    p-norm property class.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super().__init__(name, parser, *args, **kwargs)
        self.basename = str(kwargs['basename'])
        self.filetype = str(kwargs['filetype'])
        self.work_dir = str(kwargs['work_dir'])
        self.stdout_file = str(kwargs['stdout_file'])
        self.object_storage_data: Dict[str, str] = kwargs['object_storage_data']

    def _serialize(self):
        return {
            "name": "file_content",
            "basename": self.basename,
            "filetype": self.filetype,
            "objectData": {
                "CONTAINER": self.object_storage_data['CONTAINER'],
                "NAME": os.path.join(self.work_dir, self.basename),
                "PROVIDER": self.object_storage_data['PROVIDER'],
                "REGION": self.object_storage_data['REGION'],
            }
        }
