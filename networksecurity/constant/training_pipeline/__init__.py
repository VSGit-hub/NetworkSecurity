import os
import sys
import numpy as np
import pandas as pd

TARGET_COLUMN="Result"
PIPELINE_NAME = "NetworkSecurity"
ARTIFACT_DIR = "Artifacts"
FILE_NAME = "phishingData.csv"

TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"


DATA_INGSTION_COLLECTION_NAME : str = "NetworkData"
DATA_INGSTION_DATABASE_NAME : str = "DBASE"
DATA_INGSTION_DIR_NAME : str = "data_ingestion"
DATA_INGSTION_FEATURE_STORE_DIR : str = "feature_store"
DATA_INGSTION_INGESTED_DIR : str = "ingested"
DATA_INGSTION_TRAIN_TEST_SPLIT_RATIO : float = 0.2
