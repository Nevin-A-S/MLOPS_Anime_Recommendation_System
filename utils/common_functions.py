import os 
import yaml
import pandas
from src.logger import get_logger
from src.custom_exception import CustomException

logger = get_logger(__name__)

def read_yaml(file_path: str) -> dict:
    """
    Reads a YAML file and returns its content as a dictionary.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            logger.info(f"YAML file {file_path} read successfully.")
            return config
    except Exception as e:
        logger.error(f"Error reading YAML file {file_path}: {e}")
        raise CustomException("Failed to read YAML file ", e)
    
def load_data(file_path: str) -> pandas.DataFrame:
    """
    Loads data from a CSV file into a pandas DataFrame.
    """
    try:
        logger.info(f"Loading data from {file_path}...")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        
        df = pandas.read_csv(file_path)
        logger.info(f"Data loaded successfully from {file_path}.")
        return df
    except Exception as e:
        logger.error(f"Error loading data from {file_path}: {e}")
        raise CustomException("Failed to load data from CSV file ", e)