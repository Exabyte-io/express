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
        self.name = "workflow"
        self.model = self.raw_data["model"]
        self.units = self.raw_data["units"]
        self.properties = [p["name"] for p in self.raw_data["model"]["method"]["data"]["perProperty"]]

    def _serialize(self):
        """
        Serialize a ML predict workflow.

        Returns:
             dict
        """
        return {
            "name": "ML Predict Property",
            "subworkflows": [
                {
                    "_id": "LCthJ6E2QabYCZqf4",
                    "units": self.units,
                    "properties": self.properties,
                    "model": self.model,
                    "app": {
                        "name": "exabyteml",
                        "summary": "exabyte machine learning engine",
                        "version": "0.2.0"
                    },
                    "name": "ML Predict Property"
                }
            ],
            "properties": self.properties,
            "units": [
                {
                    "type": "subworkflow",
                    "_id": "LCthJ6E2QabYCZqf4"
                }
            ]
        }
