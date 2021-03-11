from express.properties import BaseProperty
import os
import copy
from typing import List
from abc import abstractmethod


class WorkflowProperty(BaseProperty):
    def __init__(self, name, parser, *args, **kwargs):
        super().__init__(name, parser, *args, **kwargs)
        self.name: str = name

    @property
    def schema(self):
        return self.esse.get_schema_by_id("workflow")

    @abstractmethod
    def get_workflow_specific_config(self) -> dict:
        return {}

    def get_common_config(self) -> dict:
        config = {
            "name": self.name,
            "creator": {
                "_id": "",
                "cls": "User",
                "slug": ""
            },
            "owner": {
                "_id": "",
                "cls": "Account",
                "slug": ""
            },
            "schemaVersion": "0.2.0",
            "exabyteId": "",
            "hash": "",
            "_id": "",
        }
        return config

    def _serialize(self) -> dict:
        config = self.get_common_config()
        config.update(self.get_workflow_specific_config())
        return config


class PyMLTrainAndPredictWorkflow(WorkflowProperty):
    """
    Quick implementation of the new version of ExabyteML
    """

    def __init__(self, name, parser, *args, **kwargs):
        """
        Constructor for PyMLTrainAndPredictWorkflow

        Args:
            name (str): Name of the workflow
            parser (str): Parser to use with this workflow
        """
        super().__init__(name, parser, *args, **kwargs)
        self.work_dir: str = self.kwargs["work_dir"]
        self.object_storage_data: dict = self.kwargs["object_storage_data"]
        self.context_dir_relative_path: str = self.kwargs["context_dir_relative_path"]
        self.workflow: dict = copy.deepcopy(self.kwargs["workflow"])

    def _create_download_from_object_storage_input(self, basename: str) -> dict:
        """
        Generates an input for a download-from-object-storage unit

        Args:
            basename (str): The basename to copy

        Returns:
            The input for a download-from-object-storage io unit

        """
        object_storage_data = copy.deepcopy(self.object_storage_data)

        # Create path name based on whether files have a relative path
        if self.context_dir_relative_path:
            path_name = (self.work_dir, self.context_dir_relative_path, basename)
        else:
            path_name = (self.work_dir, basename)
        object_storage_data.update({"NAME": os.path.join(*path_name)})

        io_unit_input = {
            "basename": basename,
            "pathname": self.context_dir_relative_path,
            "overwrite": False,
            "objectData": object_storage_data
        }
        return io_unit_input

    def set_io_unit_filenames(self, unit: dict) -> None:
        """
        Sets the filenames to copy inside of IO units

        Args:
            unit (dict): The IO unit to update

        Returns:
            None
        """
        basenames_to_copy = os.listdir(self.context_dir_relative_path)
        io_unit_inputs = map(self._create_download_from_object_storage_input, basenames_to_copy)
        unit["input"] = list(io_unit_inputs)

    def _construct_predict_subworkflows(self, train_subworkflows: list) -> list:
        """
        Given the set of training subworkflows, converts to the subworkflows defining the predict workflow.

        Args:
            train_subworkflows (list): "subworkflows" defined in the original workflow

        Returns:
            A list of subworkflows, which define the resultant predict workflow.

        """
        # Need to deepcopy to avoid changing the original subworkflow
        predict_subworkflows = copy.deepcopy(train_subworkflows)

        # What the predict property was named
        predict_property_result = {"name": "workflow:pyml_predict"}

        for unit in [subworkflow["units"] for subworkflow in predict_subworkflows]:
            # Set predict status
            if unit["flowchartId"] == "head-set-predict-status":
                unit["value"] = "True"

            # Set download-from-object-storage units
            elif unit["flowchartId"] == "head-fetch-trained-model":
                self.set_io_unit_filenames(unit)

            # Remove workflow property, so predict runs don't return another workflow
            elif predict_property_result in unit["results"]:
                unit["results"].remove(predict_property_result)

        return predict_subworkflows

    def get_workflow_specific_config(self) -> dict:
        """
        Generates the specific config for the new implementation of ExabyteML. The remainder of the config is
        generated inside of the parent Workflow class.

        Returns:
             dict
        """
        # Construct the "units" key inside the workflow. Here (and only here), "units" actually means "subworkflows,"
        # because that's what the key is called inside "workflow"
        train_subworkflow_units: list = self.workflow["units"]

        # Construct the "subworkflows" key inside the workflow
        train_subworkflows: list = self.workflow["subworkflows"]
        predict_subworkflows = self._construct_predict_subworkflows(train_subworkflows)

        specific_config = {
            "units": train_subworkflow_units,
            "subworkflows": predict_subworkflows,
        }

        return specific_config


# Todo: This is the old implementation of ExabyteML
class ExabyteMLPredictWorkflow(WorkflowProperty):
    """
    Legacy implementation of Exabyte ML's predict Workflow property class.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super().__init__(name, parser, *args, **kwargs)

        self.model = self.parser.model
        self.targets = self.parser.targets
        self.features = self.parser.features
        self.scaling_params_per_feature = self.parser.scaling_params_per_feature

    def get_workflow_specific_config(self) -> dict:
        """
        Generates the specific config for a legacy ExabyteML workflow. The remainder of the config is generated
        inside of the parent Worfklow class.

        Returns:
             dict
        """
        specific_config = {
            "units": [
                {
                    "_id": "LCthJ6E2QabYCZqf4",
                    "name": "ml_predict_subworkflow",
                    "type": "subworkflow",
                    "flowchartId": "subworkflow",
                    "head": True
                }
            ],
            "subworkflows": [
                {
                    "name": "ml_predict_subworkflow",
                    "isDraft": True,
                    "application": {
                        "version": "0.2.0",
                        "summary": "Exabyte Machine Learning Engine",
                        "name": "exabyteml",
                        "shortName": "ml",
                        "build": "Default"
                    },
                    "units": [
                        {
                            "status": "idle",
                            "statusTrack": [],
                            "head": True,
                            "flowchartId": "io",
                            "name": "input",
                            "application": {
                                "version": "0.2.0",
                                "summary": "Exabyte Machine Learning Engine",
                                "name": "exabyteml",
                                "shortName": "ml",
                                "build": "Default"
                            },
                            "results": [],
                            "next": "data_transformation_manipulation",
                            "source": "api",
                            "postProcessors": [],
                            "preProcessors": [],
                            "subtype": "dataFrame",
                            "input": [
                                {
                                    "endpoint": "dataframe",
                                    "endpoint_options": {
                                        "headers": {},
                                        "data": {
                                            "features": self.features,
                                            "ids": [],
                                            "targets": self.targets
                                        },
                                        "method": "POST",
                                        "params": {},
                                        "jobId": ""
                                    }
                                }
                            ],
                            "type": "io",
                            "monitors": []
                        },
                        {
                            "status": "idle",
                            "statusTrack": [],
                            "head": False,
                            "flowchartId": "data_transformation_manipulation",
                            "name": "clean data",
                            "monitors": [],
                            "results": [],
                            "next": "data_transformation_scale_and_reduce",
                            "application": {
                                "version": "0.2.0",
                                "summary": "Exabyte Machine Learning Engine",
                                "name": "exabyteml",
                                "shortName": "ml",
                                "build": "Default"
                            },
                            "postProcessors": [],
                            "preProcessors": [],
                            "operationType": "manipulation",
                            "operation": "data_transformation",
                            "type": "processing",
                            "inputData": {
                                "cleanMissingData": True,
                                "replaceNoneValuesWith": 0,
                                "removeDuplicateRows": True
                            }
                        },
                        {
                            "status": "idle",
                            "statusTrack": [],
                            "head": False,
                            "flowchartId": "data_transformation_scale_and_reduce",
                            "name": "scale and reduce",
                            "monitors": [],
                            "results": [],
                            "next": "score",
                            "application": {
                                "version": "0.2.0",
                                "build": "Default",
                                "name": "exabyteml",
                                "shortName": "ml",
                                "summary": "Exabyte Machine Learning Engine"
                            },
                            "postProcessors": [],
                            "preProcessors": [],
                            "operationType": "scale_and_reduce",
                            "operation": "data_transformation",
                            "type": "processing",
                            "inputData": {
                                "scaler": "standard_scaler",
                                "perFeature": self.scaling_params_per_feature,
                            }
                        },
                        {
                            "status": "idle",
                            "statusTrack": [],
                            "executable": {
                                "name": "score"
                            },
                            "flowchartId": "score",
                            "name": "score",
                            "head": False,
                            "results": [
                                {
                                    "name": "predicted_properties"
                                }
                            ],
                            "application": {
                                "version": "0.2.0",
                                "build": "Default",
                                "name": "exabyteml",
                                "shortName": "ml",
                                "summary": "Exabyte Machine Learning Engine"
                            },
                            "postProcessors": [],
                            "preProcessors": [],
                            "context": {},
                            "input": [],
                            "flavor": {
                                "name": "score"
                            },
                            "type": "execution",
                            "monitors": [
                                {
                                    "name": "standard_output"
                                }
                            ]
                        }
                    ],
                    "model": self.model,
                    "_id": "LCthJ6E2QabYCZqf4",
                    "properties": self.targets
                }
            ],
            "properties": self.targets
        }
        return specific_config
