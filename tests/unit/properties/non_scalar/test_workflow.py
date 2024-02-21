from unittest import mock

from tests.unit import UnitTestBase
from express.properties.workflow import PyMLTrainAndPredictWorkflow
from tests.fixtures.pyML.data import WORKFLOW_TRAIN, WORKFLOW_PREDICT, NAME, PARSER, ARGS, WORK_DIR, UPLOAD_DIR
from tests.fixtures.pyML.data import CONTEXT_DIR_RELATIVE_PATH, OBJECT_STORAGE_DATA, MOCK_BASENAMES


class WorkflowTest(UnitTestBase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().setUp()

    @mock.patch("express.properties.workflow.os.listdir")
    def test_pyml_workflow(self, mock_os_listdir):
        mock_os_listdir.return_value = MOCK_BASENAMES

        name = NAME
        parser = PARSER
        args = ARGS
        kwargs = {
            "work_dir": WORK_DIR,
            "upload_dir": UPLOAD_DIR,
            "object_storage_data": OBJECT_STORAGE_DATA,
            "context_dir_relative_path": CONTEXT_DIR_RELATIVE_PATH,
            "workflow": WORKFLOW_TRAIN,
        }

        property_ = PyMLTrainAndPredictWorkflow(name, parser, *args, **kwargs)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), WORKFLOW_PREDICT)
