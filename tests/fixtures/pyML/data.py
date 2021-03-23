import json
import os
from typing import Dict, List
from dataclasses import dataclass

current_path = os.path.dirname(__file__)
path = os.path.join(current_path, "test-001")
predict_workflow = "workflow_predict_after_conversion.JSON"
train_workflow = "workflow_train.JSON"

@dataclass
class Workflow_test_data:
    """
    Dataclass used cut down on the imports in the workflow test
    """
    name: str
    parser: None
    args: list
    context_dir_relative_path: str
    work_dir: str
    upload_dir: str
    mock_basenames: List[str]
    object_storage_data: Dict[str, str]
    workflow_train: Dict
    workflow_predict: Dict


# Get both workflows
with open(os.path.join(path, train_workflow), "r") as file_pointer:
    WORKFLOW_TRAIN = json.load(file_pointer)

with open(os.path.join(path, predict_workflow), "r") as file_pointer:
    WORKFLOW_PREDICT = json.load(file_pointer)

NAME = WORKFLOW_PREDICT["name"]
PARSER = None
ARGS = []

# Get basenames to mock for the os.listdirs call in test
_subworkflow_units = WORKFLOW_PREDICT["subworkflows"][0]["units"]
_download_from_s3_unit = next(filter(lambda i: i["name"] == "Fetch Trained Model as file", _subworkflow_units))
_download_from_s3_inputs = _download_from_s3_unit["input"]
MOCK_BASENAMES = [item["basename"] for item in _download_from_s3_inputs]

# Determine working directory information
_sample_object_data = _download_from_s3_inputs[0]["objectData"]
_job_context_abspath = os.path.dirname(_sample_object_data["NAME"])
CONTEXT_DIR_RELATIVE_PATH = os.path.basename(_job_context_abspath)

WORK_DIR = os.path.dirname(_job_context_abspath)
UPLOAD_DIR = WORK_DIR

# Object Storage Info
_object_storage_container = _sample_object_data["CONTAINER"]
_object_storage_provider = _sample_object_data["PROVIDER"]
_object_storage_region = _sample_object_data["REGION"]
OBJECT_STORAGE_DATA = {
    "CONTAINER": _object_storage_container,
    "NAME": "",
    "PROVIDER": _object_storage_provider,
    "REGION": _object_storage_region
}

WORKFLOW_TEST_DATA = Workflow_test_data(NAME, PARSER, ARGS, CONTEXT_DIR_RELATIVE_PATH,
                                        WORK_DIR, UPLOAD_DIR, MOCK_BASENAMES, OBJECT_STORAGE_DATA,
                                        WORKFLOW_TRAIN, WORKFLOW_PREDICT)
