import uuid
import time
import requests
from .constants import get_api_url, get_api_key, get_docs_path, get_eval_dataset_file
from .utils import read_dataset
from .exceptions import SDKException, MissingEnvironmentVariableException
import os

class EvaluatorSDK:
    def __init__(self):
        if not get_api_url() or not get_api_key():
            raise MissingEnvironmentVariableException("EVAL_API_URL or EVAL_API_KEY is not set in the environment.")
        
        self.request_data = {}
        self.request_id = None

    def get_request_data(self, request_id):
        """Retrieves the request data dictionary for a given request_id."""
        if request_id not in self.request_data:
            raise SDKException(f"Request ID {request_id} does not exist.")
        return self.request_data[request_id]

    def add_param(self, request_id, param_name, param_value):
        """Adds a parameter to the request data dictionary."""
        if request_id not in self.request_data:
            self.request_data[request_id] = {}
        
        self.request_data[request_id][param_name] = param_value

    def start_request(self):
        """Generates a unique request_id for a new request."""
        self.request_id = str(uuid.uuid4())
        return self.request_id

    def send(self, request_id):
        """Sends the collected data to the API as a POST request."""
        try:
            url = get_api_url()
            headers = {'Authorization': f"Bearer {get_api_key()}", 'Content-Type': 'application/json'}
            
            data = self.request_data.get(request_id)
            if not data:
                raise SDKException("No data found for the provided request_id.")
            
            response = requests.post(url, json=data, headers=headers, timeout=120)

            if response.status_code != 200:
                raise SDKException(f"Request failed with status code {response.status_code}: {response.text}")
            return response.json()
        except requests.exceptions.RequestException as e:
            raise SDKException(f"Request failed, An error occurred while sending data: {e}")
        except SDKException as e:
            raise SDKException(f"SDK Exception, An error occurred: {e}")
        except Exception as e:
            raise SDKException(f"Send Exception, An error occurred: {e}")

    def process_dataset(self):
        """Reads the dataset and automatically sends requests for each row."""
        if not get_eval_dataset_file():
            raise MissingEnvironmentVariableException("EVAL_DATASET_FILE is not set.")
        
        dataset = read_dataset(get_eval_dataset_file())
        for index, row in dataset.iterrows():
            request_id = self.start_request()

            # Extract parameters from the row
            self.add_param(request_id, 'project_code', row.get('project_code'))
            self.add_param(request_id, 'prompt', row.get('prompt'))
            self.add_param(request_id, 'no_of_docs_in_context', len(os.listdir(get_docs_path())))  # Example logic
            self.add_param(request_id, 'top_k', row.get('top_k'))
            self.add_param(request_id, 'no_of_docs_retrieved', row.get('no_of_docs_retrieved'))
            self.add_param(request_id, 'retrieved_ans', row.get('retrieved_ans'))
            self.add_param(request_id, 'ground_truth', row.get('ground_truth'))
            self.add_param(request_id, 'retrieved_docs_list', row.get('retrieved_docs_list'))
            self.add_param(request_id, 'total_query_time', row.get('total_query_time'))
            self.add_param(request_id, 'retrieval_time', row.get('retrieval_time'))
            self.add_param(request_id, 'generation_time', row.get('generation_time'))

            # Send the request
            response = self.send(request_id)
            print(f"Request {request_id} response: {response}")
            time.sleep(1)  # To avoid hitting rate limits or overwhelming the server

