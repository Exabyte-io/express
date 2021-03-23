import json
import os

current_path = os.path.dirname(__file__)
path = os.path.join(current_path, "test-001")
predict_workflow = "workflow_predict_after_conversion.JSON"
train_workflow = "workflow_train.JSON"

with open(os.path.join(path, train_workflow), "r") as file_pointer:
    print(file_pointer)
    WORKFLOW_TRAIN = json.load(file_pointer)

with open(os.path.join(path, predict_workflow), "r") as file_pointer:
    WORKFLOW_PREDICT = json.load(file_pointer)
