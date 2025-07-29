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
    
    def add_project_code(self, project_code):
        """Adds the project code to the request data."""
        if self.request_id is None:
            raise SDKException("Request ID is not set. Please start a request first.")
        
        self.add_param(self.request_id, 'project_code', project_code)

    def add_prompt(self, prompt):
        """Adds a prompt to the request data."""
        if self.request_id is None:
            raise SDKException("Request ID is not set. Please start a request first.")
        
        self.add_param(self.request_id, 'prompt', prompt)
    
    def add_no_of_docs_in_context(self, no_of_docs):
        """Adds the number of documents in context to the request data."""
        if self.request_id is None:
            raise SDKException("Request ID is not set. Please start a request first.")
        self.add_param(self.request_id, 'no_of_docs_in_context', no_of_docs)

    def add_top_k(self, top_k):
        """Adds the top_k parameter to the request data."""
        if self.request_id is None:
            raise SDKException("Request ID is not set. Please start a request first.")
        
        self.add_param(self.request_id, 'top_k', top_k)

    def add_no_of_docs_retrieved(self, no_of_docs):
        """Adds the number of documents retrieved to the request data."""
        if self.request_id is None:
            raise SDKException("Request ID is not set. Please start a request first.")
        
        self.add_param(self.request_id, 'no_of_docs_retrieved', no_of_docs)
    
    def add_retrieved_ans(self, retrieved_ans):
        """Adds the retrieved answers to the request data."""
        if self.request_id is None:
            raise SDKException("Request ID is not set. Please start a request first.")
        self.add_param(self.request_id, 'retrieved_ans', retrieved_ans)
    
    def add_final_ans(self, final_ans):
        """Adds the final answer to the request data."""
        if self.request_id is None:
            raise SDKException("Request ID is not set. Please start a request first.")
        
        self.add_param(self.request_id, 'final_ans', final_ans)

    def add_ground_truth(self, ground_truth):
        """Adds the ground truth to the request data."""
        if self.request_id is None:
            raise SDKException("Request ID is not set. Please start a request first.")
        
        self.add_param(self.request_id, 'ground_truth', ground_truth)
    
    def add_retrieved_docs_list(self, retrieved_docs_list):
        """Adds the list of retrieved documents to the request data."""
        if self.request_id is None:
            raise SDKException("Request ID is not set. Please start a request first.")
        self.add_param(self.request_id, 'retrieved_docs_list', retrieved_docs_list)
    
    def add_total_query_time(self, total_query_time):
        """Adds the total query time to the request data."""
        if self.request_id is None:
            raise SDKException("Request ID is not set. Please start a request first.")
        
        self.add_param(self.request_id, 'total_query_time', total_query_time)
    
    def add_retrieval_time(self, retrieval_time):
        """Adds the retrieval time to the request data."""
        if self.request_id is None:
            raise SDKException("Request ID is not set. Please start a request first.")
        
        self.add_param(self.request_id, 'retrieval_time', retrieval_time)
    
    def add_generation_time(self, generation_time):
        """Adds the generation time to the request data."""
        if self.request_id is None:
            raise SDKException("Request ID is not set. Please start a request first.")
        self.add_param(self.request_id, 'generation_time', generation_time)
    
    def add_throughput(self, throughput):
        """Adds the throughput to the request data."""
        if self.request_id is None:
            raise SDKException("Request ID is not set. Please start a request first.")
        
        self.add_param(self.request_id, 'throughput', throughput)

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
    
    def send_in_background(self):
        """Sends the collected data to the API in a separate thread."""
        import threading
        req_id = self.request_id
        if req_id is None:
            raise SDKException("Request ID is not set. Please start a request first.")
        thread = threading.Thread(target=self.send, args=(req_id,))
        thread.start()

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

