import os
import pandas as pd
import numpy as np
import joblib
from skimage.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
import sys

logger = get_logger(__name__)

class DataProcessor:
    def __init__(self,input_file,output_dir):
        self.input_file = input_file
        self.output_dir = output_dir

        self.rating_df = None
        self.anime_df = None
        self.X_Train_array = None
        self.X_test_array = None
        self.y_train = None
        self.y_test = None

        self.user2user_encoded = {}
        self.user2user_decoded = {}
        self.anime2anime_encoded = {}
        self.anime2anime_decoded = {}

        os.makedirs(self.output_dir,exist_ok=True)
        logger.info("Data Processing Initialised")
        
    def load_data(self,usecols):
        try:    
            self.rating_df = pd.read_csv(self.input_file,low_memory=True , usecols=usecols)
            logger.info("Data Loaded Sucessfully for data processing")
        except Exception as e:
            logger.error("Error Occured during data loading")
            raise CustomException("Error Occured during data loading",e)
    
    def filter_users(self,min_rating = 400):
        try:
            