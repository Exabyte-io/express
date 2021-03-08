from express.properties import BaseProperty
import os
import copy


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
        self.obj_storage_container = self.kwargs["OBJ_STORAGE_CONTAINER"]
        self.obj_storage_container_region = self.kwargs["OBJ_STORAGE_REGION"]
        self.obj_storage_container_platform = self.kwargs["CONTAINER_PLATFORM"]
        self.workflow = copy.deepcopy(workflow)

    @property
    def schema(self):
        # Shadows the schema property in BaseProperty
        # Not entirely sure why this is done in the old one, but the net effect is this avoids a call to
        #   self.esse.get_property_manifest(self.name)
        return self.esse.get_schema_by_id("workflow")

    def _create_download_from_object_storage(self, filename: str, nextUnit: str) -> dict:
        """
        Constructs the download_from_object_storage unit for use in the workflow

        Args:
            filename: Name to be given to the file when it is downloaded.
            container: Container that ran the job that resulted in the file
            source_path: Path to where the job put the file
            provider: Cloud compute provider
            region: Region of the cloud provider's server
            overwrite: If a file with the same name already exists in the destination directory, whether to replace it

        Returns:
            A download_from_object_storage workflow unit.

        """
        unit = {"filename": filename,
                "overwrite": False,
                "objectData": {"CONTAINER": self.obj_storage_container,
                               "NAME": os.path.join(self.work_dir, filename),
                               "PROVIDER": self.obj_storage_container_platform,
                               "REGION": self.obj_storage_container_region
                               },
                "flowchartID": "download-files-from-object-storage",
                "head": True,
                "name": "download_files",
                "type": "download_from_object_storage",
                "next": nextUnit
                }
        return unit

    @staticmethod
    def _find_head_flowchart_id(units: list) -> str:
        """
        Given a set of subworkflows or units, will find the head unit.

        Args:
            units: Either a subworkflow or a unit

        Returns:
            A string representing the flowchartID of the head subworkflow

        """
        # Not sure yet of the type of subworkflow_units["head"]
        # ToDo: Figure out which we expect, and remove this if/else
        if isinstance(str, units[0]["head"]):
            head_test = lambda unit: unit["head"].lower() == "true"
        else:
            head_test = lambda unit: unit["head"] == True
        # Check for the head unit where "next" is true
        head_unit = next(filter(head_test, units))
        head_unit_flowchartID = head_unit["flowchartID"]
        return head_unit_flowchartID

    def _construct_predict_subworkflows(self, train_subworkflows: list, head_subworkflow_flowchart_id: str) -> list:
        """
        Given the set of training subworkflows, converts to the subworkflows defining the predict workflow.

        Args:
            train_subworkflows: "subworkflows" defined in the original workflow
            head: Which subworkflow unit is the head unit

        Returns:
            A list of subworkflows, which define the resultant predict workflow.

        """
        # Need to deepcopy to avoid changing the original subworkflow
        predict_subworkflows = copy.deepcopy(train_subworkflows)

        # Iterate over subworkflows
        for subworkflow in predict_subworkflows:
            # Modify the head subworkflow, placing download_from_object_storage at the head
            if subworkflow["flowchartID"] == head_subworkflow_flowchart_id:
                # Find the head unit
                head_unit_flowchart_id = self._find_head_flowchart_id(subworkflow["units"])

                # Modify the previous head unit to point to the new download unit
                for unit in subworkflow["units"]:
                    if unit["flowchartID"] == head_unit_flowchart_id:
                        unit["head"] = False
                        unit["next"] = "download-files-from-object-storage"

                # Create the download_from_object_storage unit
                # Todo: Determine which files to copy (do we do this from settings.py?)
                download_unit = self._create_download_from_object_storage(filename=self.filename,
                                                                          nextUnit=head_unit_flowchart_id)
                # Add the download unit to the current set of units
                subworkflow["units"]: list
                subworkflow["units"].append(download_unit)

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

    @property
    def _serialize(self):
        """
        Creates the actual ML Predict workflow that will be output from a job. Intended for the quick implementation.
        """
        # Construct the "units" key inside the workflow. Here (and only here), "units" actually means "subworkflows,"
        # because that's what the key is called inside "workflow"
        train_subworkflow_units: list = self.workflow["units"]
        predict_subworkflow_units = self._construct_predict_subworkflow_units(train_subworkflow_units)

        # Determine which subworkflow is currently at the head
        head_subworkflow_flowchartid = self._find_head_flowchart_id(train_subworkflow_units)

        # Construct the "subworkflows" key inside the workflow
        train_subworkflows: list = self.workflow["subworkflows"]
        predict_subworkflows = self._construct_predict_subworkflows(train_subworkflows,
                                                                    head_subworkflow_flowchart_id=head_subworkflow_flowchartid)

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
