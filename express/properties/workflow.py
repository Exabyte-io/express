from express.properties import BaseProperty
import os
import copy
from typing import Dict, Any


class WorkflowProperty(BaseProperty):
    """
    Base class for workflow properties extracted in Express
    """

    def __init__(self, name: str, parser, *args, **kwargs):
        """
        Constructor for PyMLTrainAndPredictWorkflow

        Args:
            name (str): Name of the workflow
            parser (str): Parser to use with this workflow
        """
        super().__init__(name, parser, *args, **kwargs)
        self.name = name
        self.display_name = name

    @property
    def schema(self):
        return self.esse.get_schema_by_id("workflow")

    @property
    def workflow_specific_config(self) -> dict:
        return {}

    @property
    def common_config(self) -> dict:
        config = {
            "name": self.name,
            "displayName": self.display_name,
            "creator": {"_id": "", "cls": "User", "slug": ""},
            "owner": {"_id": "", "cls": "Account", "slug": ""},
            "schemaVersion": "0.2.0",
            "exabyteId": "",
            "hash": "",
            "_id": "",
        }
        return config

    def _serialize(self) -> dict:
        config = self.common_config
        config.update(self.workflow_specific_config)
        return config


class PyMLTrainAndPredictWorkflow(WorkflowProperty):
    """
    We expect workflows to have a format as follows:

    Workflow_Head_Subworkflow - Contains various units which prepare an ML job. For example, we may have the following
    units present.
        - An Assignment unit specifying whether the workflow is in Train or Predict mode (head-set-predict-status)
        - An IO unit to copy in the training set
        - A Conditional unit that specifies whether the train or predict setup is to be used
        - An IO unit to copy in the trained model if running in predict mode


    The final IO unit in the predict setup that we discuss, which copies in files needed for the workflow to function,
    is populated by this class's _create_download_from_object_storage_input function. It obtains a list of files
    the user has deemed important-enough to save in the workflow, and ensures they're around for the predict job.

    Workflow_Tail_Subworkflow - Contains the actual ML that the user wants to perform. The intention is that this is
    the more user-modifiable part of the ML feature. We might contain the following units here:
        - pyml:setup_variables_packages: A setup file that helps the user communicate the files needed in subsequent
                                         predict runs
        - pyml:data_input:read_csv:pandas: Uses Pandas to read in a CSV for use in further ML
        - pyml:pre_processing:standardization:sklearn: Scales the data such that it has mean=0 and variance=1, then
                                                       saves the scaler for use in predict workflows
        - pyml:model:multilayer_perceptron:sklearn: A multilayer perceptron being fit to a regression problem. Saves
                                                    the model to be used again in predict workflows
        - pyml:post_processing:parity_plot:matplotlib: Creates a parity plot if the workflow is in "Training" mode.
    """

    _RUNTIME_ITEM_KEYS = ("preProcessors", "postProcessors", "monitors", "results")
    _RUNTIME_ITEM_CONTAINERS = ("flavor", "executable")

    def __init__(
        self,
        name: str,
        parser,
        *args,
        work_dir: str,
        upload_dir: str,
        object_storage_data: Dict[str, str],
        context_dir_relative_path: str,
        workflow: Dict[str, Any],
        **kwargs,
    ):
        """
        Constructor for PyMLTrainAndPredictWorkflow

        Args:
            name (str): Name of the workflow
            parser (Any): Parser to use with this workflow
            work_dir (str): The working directory for the job calling Express
            context_dir_relative_path (str): Relative path, from the job's working dir, to the context directory
            object_storage_data (dict): Information about the object storage provider being usec for file I/O
            workflow (dict): The workflow used to run the job
        """
        super().__init__(name, parser, *args, **kwargs)
        self.work_dir = work_dir
        self.upload_dir = upload_dir
        self.object_storage_data = object_storage_data
        self.context_dir_relative_path = context_dir_relative_path
        self.workflow = copy.deepcopy(workflow)
        self.display_name = f"[Predict Workflow] {self.workflow['name']}"

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
            path_name = (self.upload_dir, self.context_dir_relative_path, basename)
        else:
            path_name = (self.upload_dir, basename)
        object_storage_data.update({"NAME": os.path.join(*path_name)})

        io_unit_input = {
            "type": "object_storage",
            "basename": basename,
            "pathname": self.context_dir_relative_path,
            "overwrite": False,
            "objectData": object_storage_data,
        }
        return io_unit_input

    @classmethod
    def _normalize_runtime_items(cls, items):
        if not isinstance(items, list):
            return items
        return [{"name": item} if isinstance(item, str) else item for item in items]

    @classmethod
    def _normalize_runtime_items_container(cls, container):
        if not isinstance(container, dict):
            return
        for key in cls._RUNTIME_ITEM_KEYS:
            if key in container:
                container[key] = cls._normalize_runtime_items(container[key])
            else:
                container[key] = []

    @classmethod
    def _normalize_unit(cls, unit):
        if not isinstance(unit, dict):
            return
        for key in cls._RUNTIME_ITEM_KEYS:
            if key in unit:
                unit[key] = cls._normalize_runtime_items(unit[key])
        for container_key in cls._RUNTIME_ITEM_CONTAINERS:
            if container_key in unit:
                cls._normalize_runtime_items_container(unit[container_key])
        if unit.get("type") == "execution":
            cls._normalize_execution_unit(unit)
        if unit.get("type") == "io" and unit.get("source") == "object_storage":
            for item in unit.get("input", []):
                if isinstance(item, dict) and "type" not in item:
                    item["type"] = "object_storage"

    @classmethod
    def _normalize_execution_unit(cls, unit):
        if isinstance(unit.get("context"), dict) and not unit["context"]:
            unit["context"] = []

        application = unit.get("application", {})
        executable = unit.get("executable", {})
        for target in (executable, unit.get("flavor", {})):
            if not isinstance(target, dict):
                continue
            target.setdefault("applicationName", application.get("name", ""))
            target.setdefault("applicationVersion", application.get("version", ""))
            if target is not executable:
                target.setdefault("executableName", executable.get("name", ""))

        for input_item in unit.get("input", []):
            if not isinstance(input_item, dict):
                continue
            input_item.setdefault("isManuallyChanged", False)
            if "template" not in input_item:
                input_item["template"] = {
                    "_id": input_item.get("_id", ""),
                    "name": input_item.get("name", ""),
                    "content": input_item.get("content", ""),
                    "contextProviders": input_item.get("contextProviders", []),
                    "applicationName": input_item.get("applicationName", application.get("name", "")),
                    "executableName": input_item.get("executableName", executable.get("name", "")),
                    "applicationVersion": input_item.get("applicationVersion", application.get("version", "")),
                }

    @classmethod
    def _normalize_workflow_units(cls, workflow_config):
        for subworkflow in workflow_config.get("subworkflows", []):
            for unit in subworkflow.get("units", []):
                cls._normalize_unit(unit)
        for unit in workflow_config.get("units", []):
            cls._normalize_unit(unit)

    def set_io_unit_filenames(self, unit: dict) -> None:
        """
        Sets the filenames to copy inside of IO units

        Args:
            unit (dict): The IO unit to update

        Returns:
            None
        """
        context_dir_absolute_path = os.path.join(self.upload_dir, self.context_dir_relative_path)
        basenames_to_copy = os.listdir(context_dir_absolute_path)
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

        for subworkflow in predict_subworkflows:
            for unit in filter(lambda i: "tags" in i, subworkflow["units"]):
                tags = unit["tags"]

                # Note: This should be the *first* thing we check for, in case we have tags that add properties.
                # Remove properties if needed
                if "remove-all-results" in tags:
                    unit["results"] = []

                # The following tags can be placed in any order:

                # Set predict status
                if "pyml:workflow-type-setter" in tags:
                    unit["value"] = "True"

                # Set download-from-object-storage units
                if "set-io-unit-filenames" in tags:
                    self.set_io_unit_filenames(unit)

                # Set predictors to print their predictions to the results tab during the predict phase
                if "creates-predictions-csv-during-predict-phase" in tags:
                    unit["results"] = [
                        {
                            "name": "file_content",
                            "basename": "predictions.csv",  # todo: We shouldn't be hardcoding this in to the flavors
                            "filetype": "csv",
                        }
                    ]

        return predict_subworkflows

    @property
    def is_using_dataset(self):
        return self.workflow.get("isUsingDataset", False)

    @property
    def workflow_specific_config(self) -> dict:
        """
        Generates the specific config for the workflow. The remainder of the config is
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
            "properties": self.workflow.get("properties", []),
            "workflows": self.workflow.get("workflows", []),
            "isUsingDataset": self.is_using_dataset,
        }

        self._normalize_workflow_units(specific_config)
        return specific_config
