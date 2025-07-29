import os
import pytest
from sdk.evaluator import EvaluatorSDK

# Setup environment variables for testing
os.environ["EVAL_API_URL"] = "https://httpbin.org/post"
os.environ["EVAL_API_KEY"] = "test_api_key"
os.environ["DOCS_PATH"] = "/tmp/docs"
os.environ["VECTORDB_PATH"] = "/tmp/vector"
os.environ["EVAL_DATASET_FILE"] = "tests/sample_dataset.json"  # create this if testing .json input

@pytest.fixture
def sdk():
    return EvaluatorSDK()

def test_start_request_creates_unique_id(sdk):
    req_id1 = sdk.start_request()
    req_id2 = sdk.start_request()
    assert req_id1 != req_id2
    # assert req_id1 in sdk._requests
    # assert req_id2 in sdk._requests

def test_add_param_and_data_integrity(sdk):
    req_id = sdk.start_request()
    sdk.add_param(req_id, "project_code", "PRJ123")
    sdk.add_param(req_id, "prompt", "What is AI?")
    sdk.add_param(req_id, "top_k", 5)

    data = sdk.get_request_data(req_id)
    assert data["project_code"] == "PRJ123"
    assert data["prompt"] == "What is AI?"
    assert data["top_k"] == 5

def test_send_method_success(sdk):
    req_id = sdk.start_request()
    sdk.add_param(req_id, "project_code", "PRJ456")
    sdk.add_param(req_id, "prompt", "Define machine learning.")

    response = sdk.send(req_id)
    assert response.status_code == 200
    assert "json" in response.json()

def test_send_raises_error_for_missing_request(sdk):
    with pytest.raises(ValueError, match="Invalid request ID"):
        sdk.send("non-existent-id")

def test_add_param_invalid_key(sdk):
    req_id = sdk.start_request()
    with pytest.raises(ValueError):
        sdk.add_param(req_id, "", "some_value")

def test_process_dataset_json(sdk, tmp_path):
    # Create a temporary JSON file
    sample_data = [
        {"project_code": "PRJ001", "prompt": "Test 1"},
        {"project_code": "PRJ002", "prompt": "Test 2"},
    ]
    json_path = tmp_path / "sample.json"
    import json
    with open(json_path, "w") as f:
        json.dump(sample_data, f)

    os.environ["EVAL_DATASET_FILE"] = str(json_path)
    sdk.process_dataset()  # Should run without error
