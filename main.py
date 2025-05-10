from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainingConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.components.data_validataion import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

import sys

if __name__=='__main__':
    try:
        traningpipelieconfig = TrainingPipelineConfig()
       
        data_ingestion_config = DataIngestionConfig(traningpipelieconfig)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info('initiate data ingestion')
       
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data ingetion completed")
        print(data_ingestion_artifact)
       
        data_validation_config = DataValidationConfig(traningpipelieconfig)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        logging.info("Initiated data validation")
       
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data validation completed")
        print(data_validation_config)
        
        data_transformation_config = DataTransformationConfig(traningpipelieconfig)
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Data Transformation completed")
        print(data_transformation_artifact)


        logging.info("Model Training started")
        model_trainer_config = ModelTrainingConfig(traningpipelieconfig)
        model_tainer = ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_tainer.initiate_model_trianer()
        logging.info("Model training Completed")

    except Exception as e:
        raise NetworkSecurityException(e,sys)