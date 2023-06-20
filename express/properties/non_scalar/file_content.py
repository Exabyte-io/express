import os
from typing import Dict, Any

from . import NonScalarProperty


class FileContent(NonScalarProperty):
    """
    file_content property.
    Args:
        name (str): Name of the property
        parser (Any): Express parser being used
        basename (str): the file name, without the path
        filetype (str): text or image
        upload_dir (str): Path Express sees to the working directory where the job file exists
        object_storage_data (dict): describes the object in the bucket, with keys:
            - CONTAINER (str): the name of the object store bucket
            - NAME (str): the object name in the container
            - PROVIDER (str): the cloud provider where the container exists
            - REGION (str): the cloud provider region in which the container exists
    """

    def __init__(
        self,
        name: str,
        parser: Any,
        *args,
        basename: str,
        filetype: str,
        upload_dir: str,
        object_storage_data: Dict[str, str],
        **kwargs,
    ):
        super().__init__(name, parser, *args, **kwargs)
        self.basename = basename
        self.filetype = filetype
        self.upload_dir = upload_dir
        self.object_storage_data: Dict[str, str] = object_storage_data

    def _serialize(self) -> Dict:
        return {
            "name": "file_content",
            "basename": self.basename,
            "filetype": self.filetype,
            "objectData": {
                "CONTAINER": self.object_storage_data["CONTAINER"],
                "NAME": os.path.join(self.upload_dir, self.basename),
                "PROVIDER": self.object_storage_data["PROVIDER"],
                "REGION": self.object_storage_data["REGION"],
            },
        }
