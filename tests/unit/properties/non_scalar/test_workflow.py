import mock
import os

from tests.unit import UnitTestBase
from express.properties.workflow import PyMLTrainAndPredictWorkflow
from tests.fixtures.pyML.data import WORKFLOW_TEST_DATA
import json


class WorkflowTest(UnitTestBase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().setUp()

    @mock.patch('express.properties.workflow.os')
    def test_pyml_workflow(self, mock_os):
        mock_os.listdir.return_value = WORKFLOW_TEST_DATA.mock_basenames

        name = WORKFLOW_TEST_DATA.name
        parser = WORKFLOW_TEST_DATA.parser
        args = WORKFLOW_TEST_DATA.args
        kwargs = {
            "work_dir": WORKFLOW_TEST_DATA.work_dir,
            "upload_dir": WORKFLOW_TEST_DATA.upload_dir,
            "object_storage_data": WORKFLOW_TEST_DATA.object_storage_data,
            "context_dir_relative_path": WORKFLOW_TEST_DATA.context_dir_relative_path,
            "workflow": WORKFLOW_TEST_DATA.workflow_train
        }

        property_ = PyMLTrainAndPredictWorkflow(name, parser, *args, **kwargs)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), WORKFLOW_TEST_DATA.workflow_predict)
