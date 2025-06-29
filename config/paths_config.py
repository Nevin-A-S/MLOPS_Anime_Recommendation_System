import os

################ DATA INGESTION ################

RAW_DIR = "artifacts/raw"
CONFIG_PATH = "config/config.yaml"

################ DATA PROCESSING ################

PROCESSED_DIR = 'artifacts/processsed'
ANIMELIST_CSV = "artifacts/raw/animelist.csv"
ANIME_CSV = "artifacts/raw/anime.csv"
ANIME_SYNOPSIS_CSV = "artifacts/raw/anime_with_synopsis.csv"

X_TRAIN_ARRAY = os.path.join(PROCESSED_DIR,"X_train_array.pkl")
X_TEST_ARRAY = os.path.join(PROCESSED_DIR,"X_test_array.pkl")
Y_TRAIN = os.path.join(PROCESSED_DIR,"y_train.pkl")
Y_TEST = os.path.join(PROCESSED_DIR,"y_test.pkl")

RATING_DF = os.path.join(PROCESSED_DIR,"rating_df.csv")
DF_PATH = os.path.join(PROCESSED_DIR,"anime_df.csv")
SYNPOSIS_DF_PATH = os.path.join(PROCESSED_DIR,"synposis_df.csv")

USER2USER_ENCODED  = "artifacts/processsed/user2user_encoded.pkl"
USER2USER_DECODED = "artifacts/processsed/user2user_decoded.pkl"

ANIME2ANIME_ENCODED = "artifacts/processsed/anime2anime_encoded.pkl"
ANIME2ANIME_DECODED = "artifacts/processsed/anime2anime_decoded.pkl"