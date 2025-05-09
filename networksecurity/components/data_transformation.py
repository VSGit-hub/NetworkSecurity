import os
import sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_object


class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact, data_transformation_config: DataTransformationConfig):
        try:
                self.data_validation_artifact: DataValidationArtifact = data_validation_artifact
                self.data_transformation_config: DataTransformationConfig = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try: 
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def get_data_transformer_object(cls) -> Pipeline:
        logging.info("Entered get_data_transformer_objec method of Transformation clsas")
        try:
            knn_imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"Initialzed KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            processor: Pipeline=Pipeline([("imputer", knn_imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Enterd the data transformation stage")
        try:
            logging.info("Started data transformation")
            train_dataframe = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_dataframe = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            ## Training dataframe
            input_feature_trian_df=train_dataframe.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df=train_dataframe[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1, 0) # replace -1 with 0 for classification purpose

            ## Training dataframe
            input_feature_test_df=test_dataframe.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df=test_dataframe[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0) # replace -1 with 0 for classification purpose
            
            pre_processor =self.get_data_transformer_object()
            preprocessor_obj=pre_processor.fit(input_feature_trian_df)
            transformed_input_train_feature=preprocessor_obj.transform(input_feature_trian_df)
            transformed_input_test_feature=preprocessor_obj.transform(input_feature_test_df)

            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]

            ## Save numpy array 
            save_numpy_array_data(self.data_transformation_config.transformed_train_filepath, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_filepath, array=test_arr)
            save_object(self.data_transformation_config.transformed_object_filepath,  preprocessor_obj)
        
            ## Preparing artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_filepath=self.data_transformation_config.transformed_object_filepath,
                transformed_train_filepath=self.data_transformation_config.transformed_train_filepath,
                transfromed_test_filepath=self.data_transformation_config.transformed_test_filepath
                )
            return data_transformation_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)