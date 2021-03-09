from express.properties import BaseProperty
import os
import copy
from typing import List


# Note for naming convention: code uses snake_case, JSON uses camelCase


# Todo: This is the quick implementation of ExabyteML, and will be depreciated eventually
class MLQuickImplementation(BaseProperty):
    """
    Quick implementation of the new version of ExabyteML
    """

    def __init__(self, name, parser, *args, **kwargs):
        """
        Constructor for MLQuickImplementation

        Args:
            name (str): Name of the workflow
            parser (str): Parser to use with this workflow
        """
        super().__init__(name, parser, *args, **kwargs)
        self.name = name
        self.work_dir = self.kwargs["work_dir"]

        object_storage_data = self.kwargs["object_storage_data"]
        self.obj_storage_container = object_storage_data["CONTAINER"]
        self.obj_storage_container_region = object_storage_data["REGION"]
        self.obj_storage_container_provider = object_storage_data["PROVIDER"]
        self.ml_cache_dir = ".mlcache"
        self.workflow = copy.deepcopy(self.kwargs["workflow"])

    @property
    def schema(self):
        # Shadows the schema property in BaseProperty
        # Not entirely sure why this is done in the old one, but the net effect is this avoids a call to
        #   self.esse.get_property_manifest(self.name)
        return self.esse.get_schema_by_id("workflow")

    def _create_download_from_object_storage_inputs(self, filenames: List[str]) -> list:
        """
        Constructs the download_from_object_storage unit for use in the workflow

        Args:
            filenames: List of filenames to copy in
            ml_cache_dir: Where the pickles are being stored

        Returns:
            A download_from_object_storage workflow unit.

        """
        inputs = []
        if isinstance(filenames, str):
            # Ensure we have a list of strings
            filenames = [filenames]

        for filename in filenames:
            # If ml_cache_dir is defined (e.g. we're not just pickling to the job's root dir), make sure it's in the path
            if self.ml_cache_dir:
                path_names = (self.work_dir, self.ml_cache_dir, filename)
            else:
                path_names = (self.work_dir, filename)

            inputs.append({"basename": filename,
                           "pathname": self.ml_cache_dir,
                           "overwrite": False,
                           "objectData": {"CONTAINER": self.obj_storage_container,
                                          "NAME": os.path.join(*path_names),
                                          "PROVIDER": self.obj_storage_container_provider,
                                          "REGION": self.obj_storage_container_region
                                          }
                           })
        return inputs

    def _construct_predict_subworkflows(self, train_subworkflows: list) -> list:
        """
        Given the set of training subworkflows, converts to the subworkflows defining the predict workflow.

        Args:
            train_subworkflows: "subworkflows" defined in the original workflow

        Returns:
            A list of subworkflows, which define the resultant predict workflow.

        """
        # Need to deepcopy to avoid changing the original subworkflow
        predict_subworkflows = copy.deepcopy(train_subworkflows)

        # Tiers need to present to make it through ESSE validations
        tiers = {"tier1": "statistical",
                 "tier2": "deterministic",
                 "tier3": "machine_learning"}
        for subworkflow in predict_subworkflows:
            subworkflow["model"].update(tiers)

            for unit in subworkflow["units"]:
                # Set download-from-object-storage units
                if unit["flowchartId"] == "head-fetch-trained-model":
                    # Update with the pickles to copy
                    filenames = os.listdir(self.ml_cache_dir)
                    download_inputs = self._create_download_from_object_storage_inputs(filenames)
                    unit["input"] = download_inputs

                # Set predict status
                elif unit["flowchartId"] == "head-set-predict-status":
                    # Set IS_PREDICT to True
                    # Needs to be string True, otherwise this gets converted to "true" in the JSON, and will fail
                    # in SimpleEval when Rupy runs the unit again later
                    unit["value"] = "True"

                # Remove workflow property, so predict runs don't return another workflow
                elif {"name": "workflow:pyml_predict"} in unit["results"]:
                    unit["results"].remove({"name": "workflow:pyml_predict"})


        return predict_subworkflows

    def _construct_predict_subworkflow_units(self, train_subworkflow_units: list) -> list:
        """
        Constructs the predict subworkflow units, for use in the generated predict workflow.
        Here, and only here, "units" is intended to mean "subworkflows," because that's what the Workflows object
        uses to define the subworkflow graph.

        Args:
            train_subworkflow_units: "Units" defined in the original workflow.

        Returns:
            A list describing the order in which subworkflows will be executed.
        """
        # Todo: Implement the way we'll construct the subworkflow units below
        return train_subworkflow_units

    def _serialize(self):
        """
        Creates the actual ML Predict workflow that will be output from a job. Intended for the quick implementation.
        """
        # Construct the "units" key inside the workflow. Here (and only here), "units" actually means "subworkflows,"
        # because that's what the key is called inside "workflow"
        train_subworkflow_units: list = self.workflow["units"]
        predict_subworkflow_units = self._construct_predict_subworkflow_units(train_subworkflow_units)

        # Construct the "subworkflows" key inside the workflow
        train_subworkflows: list = self.workflow["subworkflows"]
        predict_subworkflows = self._construct_predict_subworkflows(train_subworkflows)

        # Create the workflow
        workflow = {
            # Contents of the workflow:
            "units": predict_subworkflow_units,
            "subworkflows": predict_subworkflows,  # Units which make up each subworkflow are found here

            # Metadata describing the workflow
            "name": self.name,  # Friendly name for the workflow
            "creator": {  # Information about the account that created this workflow ("" for automatic filling)
                "_id": "",
                "cls": "User",
                "slug": ""
            },
            "owner": {  # Information about the account that currently owns this workflow ("" for automatic filling)
                "_id": "",
                "cls": "Account",
                "slug": ""
            },
            "schemaVersion": "0.2.0",  # Version of this schema to use in ESSE
            "exabyteId": "",  # ID for the corresponding bank workflow. Leave as the empty string.
            "hash": "",  # Hash used to compare workflows for uniqueness. Leave as the empty string.
            "_id": "",  # ID for MongoDB; needs to be blank. Leave as the empty string.
        }

        return workflow


# Todo: This is the old implementation of ExabyteML
class ExabyteMLPredictWorkflow(BaseProperty):
    """
    Exabyte ML predict Workflow property class.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(ExabyteMLPredictWorkflow, self).__init__(name, parser, *args, **kwargs)
        self.name = name
        self.model = self.parser.model
        self.targets = self.parser.targets
        self.features = self.parser.features
        self.scaling_params_per_feature = self.parser.scaling_params_per_feature

    def _serialize(self):
        """
        Serialize a ML predict workflow.

        Returns:
             dict
        """
        return {
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
            "name": self.name,
            "properties": self.targets,
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

    @property
    def schema(self):
        return self.esse.get_schema_by_id("workflow")
