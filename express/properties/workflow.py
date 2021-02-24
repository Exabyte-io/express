from express.properties import BaseProperty
import copy


# Todo: This is the quick implementation of ExabyteML, and will be depreciated eventually
class MLQuickImplementation(BaseProperty):
    """
    Quick implementation of the new version of ExabyteML
    """

    def __init__(self, name, parser, workflow, *args, **kwargs):
        """
        Constructor for MLQuickImplementation

        Args:
            name (str): Name of the workflow
            parser (str): Parser to use with this workflow
            workflow (dict): JSON containing the workflow itself
        """
        super(MLQuickImplementation, self).__init__(name, parser, *args, **kwargs)
        self.name = name
        self.workflow = copy.deepcopy(workflow)

    @property
    def schema(self):
        return self.esse.get_schema_by_id("workflow")

    # Todo: Implement this
    def _process_unit(self, unit: dict) -> dict:
        """
        Takes a workflow unit from a train workflow, and converts it to the corresponding predict workflow unit.
        Args:
            unit (dict): The unit to be converted

        Returns:
            A dictionary of the predict workflow unit
        """
        unit = copy.deepcopy(unit)
        return unit

    def _process_subworkflow(self, subworkflow: dict) -> dict:
        """
        Takes a train workflow and converts it to a predict workflow.

        Args:
            subworkflow (dict): The subworkflow to be converted

        Returns:
            A dictionary of the predict subworkflow
        """
        subworkflow = copy.deepcopy(subworkflow)

        # Rename the subworkflow units
        # Mapping of the form {TrainWorkflowName : PredictWorkflowName}
        name_mapping = {"SetupJob": "SetupJob",
                        "PreProcessData": "PreProcessData",
                        "TrainModel": "Predict",
                        "DrawPlots": "DrawPlots"}
        name = subworkflow["name"]
        subworkflow["name"] = name_mapping[name]

        # Change the subworkflow units
        new_units = map(self._process_unit, subworkflow["units"])
        subworkflow["units"] = list(new_units)
        return subworkflow

    @property
    def _serialize(self):
        """
        Creates the actual ML Predict workflow that will be output from a job. Intended for the quick implementation.

        We assume that all predict workflows in this implementation will contain the following subworkflows:
        1) SetupJob
            Contains directives which set up the job. Configuration, copying data, installing packages, etc.
        2) PreProcessData
            First unit is IO to load data. Subsequent units include things like normalization, standardization, etc.
        3) TrainModel
            We deliberately skip the "hyperparameter optimization" step, since we already have a trained model
            This will get re-named to "Predict" by process_subworkflow
        4) DrawPlots
            Saves any plots that may have been generated during the job.
        """
        # A note on variable naming conventions, since this code intersects two different conventions.
        # In the Python code, we're sticking with snake_case for variables.
        # In our JSON (e.g. things we define in ESSE), we stick with CamelCase for variable names.
        valid_subworkflow_names = ["SetupJob", "PreProcessData", "TrainModel", "DrawPlots"]
        subworkflows: list = self.workflow["subworkflows"]
        valid_subworkflows = filter(lambda subworkflow: True if subworkflow["name"] in valid_subworkflow_names else False,
                                    subworkflows)
        processed_subworkflows = map(self._process_subworkflow, valid_subworkflows)
        # Create the workflow
        workflow = {
            # These "
            "units": [
                {
                    # Per the 2/24 morning standup, it looks like _id should be fine this way, as long as
                    # we only refer to it internally in this workflow. The problem of unique ID's becomes a bigger deal
                    # when we store the workflow in MongoDB. For this reason, we're leaving the top-level
                    # workflow["_id"] field as the empty string.
                    "_id": "SetupJob",  # Some unique ID (internally) for the subworkflow
                    "name": "SetupJob",  # Friendly, human-readable name for the subworkflow
                    "type": "subworkflow",
                    "flowchartId": "SetupJob",  # How to refer to this subworkflow in the "next" key
                    "head": True,  # Whether this is the first subworkflow to be used
                    "next": "PreProcessData"  # The flowchartId of the next subworkflow in the series
                },
                {
                    "_id": "PreProcessData",
                    "name": "PreProcessData",
                    "type": "subworkflow",
                    "flowchartId": "PreProcessData",
                    "head": False,
                    "next": "Predict"
                },
                {
                    "_id": "Predict",
                    "name": "Predict",
                    "type": "subworkflow",
                    "flowchartId": "Predict",
                    "head": False,
                    "next": "DrawPlots"
                },
                {
                    "_id": "DrawPlots",
                    "name": "DrawPlots",
                    "type": "subworkflow",
                    "flowchartId": "Predict",
                    "head": False
                }
            ],
            "subworkflows": list(processed_subworkflows),  # Units which make up each subworkflow are found here
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
