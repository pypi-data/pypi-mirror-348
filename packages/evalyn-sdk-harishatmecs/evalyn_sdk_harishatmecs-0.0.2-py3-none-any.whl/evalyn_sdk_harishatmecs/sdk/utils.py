import os
import pandas as pd
import json
from .exceptions import InvalidFileFormatException

def read_dataset(file_path):
    """Reads the dataset depending on file format (Excel/JSON)."""
    if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        return pd.read_excel(file_path)
    elif file_path.endswith('.json'):
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        raise InvalidFileFormatException("Only .xlsx, .xls, and .json formats are supported.")

