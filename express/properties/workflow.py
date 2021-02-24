from express.properties import BaseProperty


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
        self.workflow = workflow

    @property
    def schema(self):
        return self.esse.get_schema_by_id("workflow")

    @staticmethod
    def process_subworkflow(subworkflow: dict) -> dict:
        return subworkflow

    def _serialize(self):
        """
        Creates the actual ML Predict workflow that will be output frmo a job. Intended for the quick implementation.

        We assume that all predict workflows in this implementation will contain the following subworkflows:
        1) SetupJob
            Contains directives which set up the job. Configuration, copying data, installing packages, etc.
        2) PreProcessData
            First unit is IO to load data. Subsequent units include things like normalization, standardization, etc.
        3) Predict
            We deliberately skip the "hyperparameter optimization" step, since we already have a trained model
        4) DrawPlots
            Saves any plots that may have been generated during the job.
        """
        valid_subworkflow_names = ["SetupJob", "PreProcessData", "Predict", "DrawPlots"]
        subworkflows: list = self.workflow["subworkflows"]
        valid_subworkflows = filter(lambda subworkflow: True if subworkflow["name"] in valid_subworkflow_names else False,
                                    subworkflows)
        processed_subworkflows = map(self.process_subworkflow, valid_subworkflows)

        # Create the workflow
        workflow = {
            # These "
            "units": [
                {
                    "_id": "SetupJob",  # Todo: Proper way to set ID? Can this be an empty string as below?
                    "name": "SetupJob",
                    "type": "subworkflow",
                    "flowchartId": "SetupJob",
                    "head": True,
                    "next": "PreProcessData"
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
            "subworkflows": list(processed_subworkflows),
            "name": self.name,
            "creator": {
                "_id": "",  # Todo: Isn't this required information?
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
