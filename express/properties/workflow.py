from express.properties import BaseProperty


class ExabyteMLPredictWorkflow(BaseProperty):
    """
    Exabyte ML predict Workflow property class.

    Args:
        raw_data (dict): raw data used to form the material.
        args (list): material-specific args.
        kwargs (dict): material-specific kwargs.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        super(ExabyteMLPredictWorkflow, self).__init__(name, raw_data, *args, **kwargs)
        self.name = name
        self.data_per_property = self.raw_data["data_per_property"]
        self.precision_per_property = self.raw_data["precision_per_property"]
        self.scaling_params_per_feature = self.raw_data["scaling_params_per_feature"]
        self.targets = [p["name"] for p in self.data_per_property]
        self.features = [f["name"] for f in self.scaling_params_per_feature]

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
                    "app": {
                        "version": "0.2.0",
                        "name": "exabyteml",
                        "summary": "exabyte machine learning engine"
                    },
                    "units": [
                        {
                            "flowchartId": "io",
                            "head": True,
                            "io": {
                                "flavor": "api",
                                "input": [
                                    {
                                        "endpoint": "dataframe",
                                        "endpoint_options": {
                                            "data": {
                                                "features": self.features,
                                                "ids": [],
                                                "targets": self.targets
                                            },
                                            "headers": {},
                                            "method": "POST",
                                            "params": {}
                                        }
                                    }
                                ],
                                "subtype": "input"
                            },
                            "monitors": [],
                            "name": "io",
                            "next": "data_transformation_manipulation",
                            "postProcessors": [],
                            "preProcessors": [],
                            "results": [],
                            "status": "idle",
                            "type": "io"
                        },
                        {
                            "flowchartId": "data_transformation_manipulation",
                            "head": False,
                            "monitors": [],
                            "name": "data_transformation_manipulation",
                            "next": "data_transformation_scale_and_reduce",
                            "postProcessors": [],
                            "preProcessors": [],
                            "processing": {
                                "flavor": "manipulation",
                                "input": {
                                    "cleanMissingData": True,
                                    "removeDuplicateRows": True,
                                    "replaceNoneValuesWith": 0
                                },
                                "operation": "data_transformation"
                            },
                            "results": [],
                            "status": "idle",
                            "type": "processing"
                        },
                        {
                            "flowchartId": "data_transformation_scale_and_reduce",
                            "head": False,
                            "monitors": [],
                            "name": "data_transformation_scale_and_reduce",
                            "next": "score",
                            "postProcessors": [],
                            "preProcessors": [],
                            "processing": {
                                "flavor": "scale_and_reduce",
                                "input": {
                                    "scaler": "standard_scaler",
                                    "perFeature": self.scaling_params_per_feature,
                                },
                                "operation": "data_transformation"
                            },
                            "results": [],
                            "status": "idle",
                            "type": "processing"
                        },
                        {
                            "execution": {
                                "app": {
                                    "exec": "score",
                                    "flavor": "score",
                                    "name": "exabyteml",
                                    "summary": "exabyte machine learning engine",
                                    "version": "0.2.0"
                                },
                                "input": []
                            },
                            "flowchartId": "score",
                            "head": False,
                            "monitors": [],
                            "name": "score",
                            "postProcessors": [],
                            "preProcessors": [],
                            "results": [],
                            "status": "idle",
                            "type": "execution"
                        }
                    ],
                    "model": {
                        "subtype": "supervised",
                        "type": "machine_learning",
                        "method": {
                            "subtype": "least_squares",
                            "type": "linear",
                            "precision": {
                                "perProperty": self.precision_per_property
                            },
                            "data": {
                                "perProperty": self.data_per_property
                            }
                        }
                    },
                    "_id": "LCthJ6E2QabYCZqf4",
                    "properties": self.targets
                }
            ],
            "name": self.name,
            "properties": self.targets
        }

    def serialize_and_validate(self):
        """
        Serialize the property and validates it against the schema.

        Returns:
            dict
        """
        instance = self._serialize()
        self.esse.validate(instance, self.esse.get_schema("workflow"))
        return instance
