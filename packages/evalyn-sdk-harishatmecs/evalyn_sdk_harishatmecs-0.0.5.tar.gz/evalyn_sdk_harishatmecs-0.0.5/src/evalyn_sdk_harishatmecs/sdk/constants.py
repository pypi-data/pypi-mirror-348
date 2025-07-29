import os

from dotenv import load_dotenv

load_dotenv()

def get_env_variable(var_name, default=None):
    """Reads an environment variable, and provides a default if not set."""
    return os.getenv(var_name, default)

EVAL_API_URL = get_env_variable('EVAL_API_URL')
DOCS_PATH = get_env_variable('DOCS_PATH')
VECTORDB_PATH = get_env_variable('VECTORDB_PATH')
EVAL_API_KEY = get_env_variable('EVAL_API_KEY')
EVAL_DATASET_FILE = get_env_variable('EVAL_DATASET_FILE')


def get_api_url():
    """Returns the API URL."""
    return get_env_variable('EVAL_API_URL')


def get_api_key():
    """Returns the API key."""
    return get_env_variable('EVAL_API_KEY')

def get_docs_path():
    """Returns the path to the documentation."""
    return get_env_variable('DOCS_PATH')

def get_vector_db_path():
    """Returns the path to the vector database."""
    return get_env_variable('VECTORDB_PATH')


def get_eval_dataset_file():
    """Returns the path to the evaluation dataset file."""
    return get_env_variable('EVAL_DATASET_FILE')

