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
