from mock import MagicMock

from tests.unit import UnitTestBase
from express.properties.workflow import PyMLTrainAndPredictWorkflow
from tests.fixtures.pyML.data import WORKFLOW_TRAIN, WORKFLOW_PREDICT

import json


class WorkflowTest(UnitTestBase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().setUp()

    def test_pyml_workflow(self):
        name = "workflow:pyml_predict"
        parser = None
        args = []
        kwargs = {
            "basename": "workflow:pyml_predict",
            "work_dir": "/cluster-001-share/groups/exaorg-ceyj3fjz/exaorg-ceyj3fjz-default/new-job-mar-23-2021-13-31-pm-clone-a7hp89FMgRHrs55ZC/",
            "upload_dir": "/cluster-001-share/groups/exaorg-ceyj3fjz/exaorg-ceyj3fjz-default/new-job-mar-23-2021-13-31-pm-clone-a7hp89FMgRHrs55ZC/",
            "object_storage_data": {
                "CONTAINER": "vagrant-cluster-001",
                "NAME": "",
                "PROVIDER": "aws",
                "REGION": "us-east-1"
            },
            "context_dir_relative_path": ".job_context",
            "workflow": WORKFLOW_TRAIN
        }
        property_ = PyMLTrainAndPredictWorkflow(name, parser, *args, **kwargs)
        print(json.dumps(property_.serialize_and_validate()))
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), WORKFLOW_PREDICT)
