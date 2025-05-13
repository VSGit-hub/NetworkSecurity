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

SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")

SAVED_MODEL_DRI: str = os.path.join("saved_model")
MODEL_FILE_NAME: str = "model.pkl"

# Constants relate to data ingestion
DATA_INGSTION_COLLECTION_NAME : str = "NetworkData"
DATA_INGSTION_DATABASE_NAME : str = "DBASE"
DATA_INGSTION_DIR_NAME : str = "data_ingestion"
DATA_INGSTION_FEATURE_STORE_DIR : str = "feature_store"
DATA_INGSTION_INGESTED_DIR : str = "ingested"
DATA_INGSTION_TRAIN_TEST_SPLIT_RATIO : float = 0.2

# Constants related to data validation
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILENAME: str = "report.yaml"
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"


# Constants for data transformation
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"
DATA_TRANSFORMATION_TRAIN_FILE_PATH: str = "train.npy"
DATA_TRANSFORMATION_TEST_FILE_PATH: str = "test.npy"
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",
}

# Constants for model Trainer
MODEL_TRAINER_DIR: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODLE_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_FILE_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THERSHOLD: float = 0.05

TRAINING_BUCKET_NAME = "networksecurityv300"