import os
from typing import Dict

from . import NonScalarProperty


class FileContent(NonScalarProperty):
    """
    file_content property.
    Args:
        **kwargs: required fields are:
                    - basename (str): the file name, without the path
                    - filetype (str): text or image
                    - work_dir (str): the working directory where the job file exists
                    - object_storage_data (dict): describes the object in the bucket, with keys:
                        - CONTAINER (str): the name of the object store bucket
                        - NAME (str): the object name in the container
                        - PROVIDER (str): the cloud provider where the container exists
                        - REGION (str): the cloud provider region in which the container exists
    """

    def __init__(self, name, parser, *args, **kwargs):
        super().__init__(name, parser, *args, **kwargs)
        self.basename = str(kwargs['basename'])
        self.filetype = str(kwargs['filetype'])
        self.work_dir = str(kwargs['work_dir'])
        self.upload_dir = str(kwargs['upload_dir'])
        self.object_storage_data: Dict[str, str] = kwargs['object_storage_data']

    def _serialize(self):
        return {
            "name": "file_content",
            "basename": self.basename,
            "filetype": self.filetype,
            "objectData": {
                "CONTAINER": self.object_storage_data['CONTAINER'],
                "NAME": os.path.join(self.upload_dir, self.basename),
                "PROVIDER": self.object_storage_data['PROVIDER'],
                "REGION": self.object_storage_data['REGION'],
            }
        }
