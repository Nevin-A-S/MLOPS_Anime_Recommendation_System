from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Embedding, Flatten, BatchNormalization,Dot,Activation
from utils.common_functions import read_yaml
from src.logger import get_logger
from src.custom_exception import CustomException

logger = get_logger(__name__)

class BaseModel:
    def __init__(self,config_path):
        try:
            self.config = read_yaml(config_path)
            logger.info("Loaded Configuration from config.yaml")
        
        except Exception as e:
            logger.error(f"Error in loading config file: {str(e)}")
            raise CustomException("Error in loading config file",e)
        
    def RecommenderNet(self,n_users,n_animes):

        try:

            embedding_size = self.config["model"]["embedding_size"]

            user = Input(name="user",shape=[1])
            user_embedding = Embedding(name= "user_embeddings",input_dim=n_users,output_dim=embedding_size)(user)

            anime = Input(name="anime",shape=[1])
            anime_embedding = Embedding(name= "anime_embeddings",input_dim=n_animes,output_dim=embedding_size)(anime)

            x = Dot(name = "Dot_product" , normalize=True,axes=2)([user_embedding,anime_embedding])
            x = Flatten()(x)

            x = Dense(1,kernel_initializer='he_normal')(x)
            x = BatchNormalization()(x)
            x = Activation("sigmoid")(x)
            
            model = Model(inputs = [user,anime],outputs = x)
            model.compile(loss=self.config["model"]["loss"], optimizer=self.config["model"]["optimizer"],metrics = self.config["model"]["metrics"])

            return model
        except Exception as e:
            logger.error(f"Error in building model: {str(e)}")
            raise CustomException("Error in building model",e)