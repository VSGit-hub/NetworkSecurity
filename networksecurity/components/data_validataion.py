from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file

from scipy.stats import ks_2samp
import pandas as pd
import os
import sys


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_number_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            number_columns = len(self.schema_config['columns'])
            dataframe_columns = len(dataframe.columns)

            logging.info(f"Required number of columns: {number_columns}")
            logging.info(f"DataFrame has columns: {dataframe_columns}")

            return number_columns == dataframe_columns
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_numerical_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            numerical_columns = list(self.schema_config['numerical_columns'])
            dataframe_all_columns = dataframe.columns
            all_exists = True

            for col in numerical_columns:
                if col not in dataframe_all_columns:
                    all_exists = False
                    break

            return all_exists
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_dataset_drift(self, base_df, current_df, threshold=0.5) -> bool:
        try:
            status = True
            report = {}

            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                result = ks_2samp(d1, d2)

                if threshold < result.pvalue:
                    is_drift = False
                else:
                    is_drift = True
                    status = False

                report[column] = {
                    "p_value": float(result.pvalue),
                    "drift_status": is_drift
                }

            drift_report_filepath = self.data_validation_config.drift_report_file_path
            os.makedirs(os.path.dirname(drift_report_filepath), exist_ok=True)
            write_yaml_file(file_path=drift_report_filepath, content=report)

            return status
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # Read the data
            train_dataframe = self.read_data(train_file_path)
            test_dataframe = self.read_data(test_file_path)

            # Validate number of columns
            if not self.validate_number_columns(train_dataframe):
                raise ValueError("Train dataframe does not contain all required columns.")

            if not self.validate_number_columns(test_dataframe):
                raise ValueError("Test dataframe does not contain all required columns.")

            # Validate numerical columns
            if not self.validate_numerical_columns(train_dataframe):
                raise ValueError("Train dataframe does not contain all numerical columns.")

            if not self.validate_numerical_columns(test_dataframe):
                raise ValueError("Test dataframe does not contain all numerical columns.")

            # Detect data drift
            status = self.detect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe)

            # Save validated data
            os.makedirs(os.path.dirname(self.data_validation_config.valid_train_data_filepath), exist_ok=True)
            train_dataframe.to_csv(self.data_validation_config.valid_train_data_filepath, index=False, header=True)
            test_dataframe.to_csv(self.data_validation_config.valid_test_data_filepath, index=False, header=True)

            # Prepare artifact
            data_validation_artifact = DataValidationArtifact(
                validataion_status=status,
                valid_train_file_path=self.data_ingestion_artifact.train_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
