import comet_ml
import joblib
import numpy as np
import os
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint,LearningRateScheduler,TensorBoard
from src.logger import get_logger
from src.custom_exception import CustomException
from src.base_model import BaseModel
from config.paths_config import *

logger = get_logger(__name__)

from dotenv import load_dotenv

load_dotenv()

comet_ml_key = os.getenv("COMET_ML_KEY")

class ModelTrainer:
    def __init__(self,data_path):
        self.data_path = data_path
        logger.info("Model Training Initialized")
        self.experiment = comet_ml.Experiment(
            api_key=comet_ml_key,
            project_name = "mlops-anime-recommendation-system",
            workspace = "nevin",
            auto_histogram_weight_logging=True,
            auto_histogram_gradient_logging=True,
            auto_histogram_activation_logging=True,
            log_env_cpu=True
        )
        logger.info("Experiment tracking initialized")


    def load_data(self):
        try:
            X_train_array = joblib.load(X_TRAIN_ARRAY)
            X_test_array = joblib.load(X_TEST_ARRAY)
            y_train = joblib.load(Y_TRAIN)
            y_test = joblib.load(Y_TEST)

            logger.info("Data Loaded sucessfully for model training")
            return X_train_array,X_test_array,y_train,y_test
        
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise CustomException("Error loading data",e)
    
    def train_model(self):
        try:
            X_train_array,X_test_array,y_train,y_test = self.load_data()
            n_users = len(joblib.load(USER2USER_ENCODED))
            n_anime = len(joblib.load(ANIME2ANIME_ENCODED))

            base_model = BaseModel(CONFIG_PATH)
            model = base_model.RecommenderNet(n_users,n_anime)
            
            start_learning_rate = 0.0001
            min_learning_rate = 0.0001
            max_learning_rate = 0.00005
            batch_size = 10000

            ramup_epoch = 5
            sustain_epoch = 0
            exp_decay = 0.8

            def lrfn(epoch):

                if epoch<ramup_epoch:
                    return(max_learning_rate-start_learning_rate)/ramup_epoch*epoch+start_learning_rate
                
                elif epoch<ramup_epoch+sustain_epoch:
                    return max_learning_rate
                
                else:
                    return (max_learning_rate-min_learning_rate)*exp_decay **(epoch-ramup_epoch-sustain_epoch) + min_learning_rate
            
            lr_callback = LearningRateScheduler(lambda epoch:lrfn(epoch),verbose=0)
            checkpoint_weight = CHECK_POINT_FILE_PATH

            model_checkpoint = ModelCheckpoint(filepath=checkpoint_weight,
                                            save_weights_only=True,
                                            monitor='val_loss',
                                            mode = 'min',
                                            save_best_only=True)

            early_stopping = EarlyStopping(patience=5,
                                        monitor = "val_loss",
                                        mode = 'min',
                                        restore_best_weights =True)

            my_callbacks = [model_checkpoint,lr_callback,early_stopping]

            os.makedirs(os.path.dirname(CHECK_POINT_FILE_PATH),exist_ok=True)
            os.makedirs(MODEL_DIR,exist_ok=True)
            os.makedirs(WEIGHTS_DIR,exist_ok=True)

            with self.experiment.train():

                history = model.fit(
                    x=X_train_array,
                    y=y_train,
                    epochs=20,
                    batch_size=batch_size,
                    verbose = 1,
                    validation_data=(X_test_array, y_test),
                    callbacks = my_callbacks
                )

            logger.info("Model Training Completed")

            self.save_model_weights(model)

        except Exception as e:
            logger.error(f"Error in training model: {e}")
            raise CustomException("Error while training the model",e)
        
    def extract_weights(self,layer_name,model):
        try:
            logger.info(f"Extracting weights for {layer_name}")
            weights_layer = model.get_layer(layer_name)
            weights = weights_layer.get_weights()[0]
            weights = weights/np.linalg.norm(weights,axis=1).reshape((-1,1))
            return weights
        except Exception as e:
            logger.error(f"Error in extracting weights: {e}")
            raise CustomException("Error while extracting weights",e)
    
    def save_model_weights(self,model):
        try:
            model.save(MODEL_PATH)
            logger.info("Model Saved")

            user_weights = self.extract_weights("user_embeddings",model)
            anime_weights = self.extract_weights("anime_embeddings",model)

            joblib.dump(user_weights,USER_WEIGHTS_PATH)
            joblib.dump(anime_weights,ANIME_WEIGHTS_PATH)

            self.experiment.log_asset(MODEL_PATH)
            self.experiment.log_asset(ANIME_WEIGHTS_PATH)
            self.experiment.log_asset(USER_WEIGHTS_PATH)

            logger.info("User and anime weights saved sucessfully")

        except Exception as e:
            logger.error(f"Error in saving model weights: {e}")
            raise CustomException("Error while saving model weights",e)
        
if __name__ =="__main__":
    model_trainer = ModelTrainer(PROCESSED_DIR)
    model_trainer.train_model()
