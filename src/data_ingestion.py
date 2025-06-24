import os
import pandas as pd
from google.cloud import storage
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config_path):
        """
        Initializes the DataIngestion class with the configuration file path.
        """
        self.config = read_yaml(config_path)
        self.bucket_name = self.config['data_ingestion']['bucket_name']
        self.file_name = self.config['data_ingestion']['bucket_file_names']
        self.raw_data_path = RAW_DIR

        os.makedirs(self.raw_data_path, exist_ok=True)

        logger.info(f"Data Ingestion initialized with bucket: {self.bucket_name} and file: {self.file_name}")
    
    def download_from_gcp(self):
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket(self.bucket_name)

            for file_name in self.file_name:

                destination_file_name = os.path.join(self.raw_data_path, file_name)

                if file_name=="animelist.csv":
                    blob = bucket.blob(file_name)
                    blob.download_to_filename(destination_file_name)

                    data = pd.read_csv(destination_file_name , nrows=5000000)
                    data.to_csv(destination_file_name, index=False)
                    logger.info(f"Downloaded {file_name} to {destination_file_name}")

                else:
                    blob = bucket.blob(file_name)
                    blob.download_to_filename(destination_file_name)
                    logger.info(f"Downloaded {file_name} to {destination_file_name}")

        except Exception as e:
            logger.error(f"Error downloading files from GCP: {e}")
            raise CustomException("Error downloading files from GCP" , e) 
    
    def run(self):
        try:
            logger.info("Starting data ingestion process...")
            self.download_from_gcp()
            logger.info("Data ingestion process completed successfully.")
        except Exception as e:
            logger.error(f"Data ingestion failed: {e}")
            raise CustomException("Data ingestion failed", e)

if __name__ == "__main__":
    data_ingestion = DataIngestion(CONFIG_PATH)
    data_ingestion.run()