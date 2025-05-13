import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validataion import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainingConfig
)

from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)

from networksecurity.cloud.s3_syncer import S3sync
from networksecurity.constant.training_pipeline import TRAINING_BUCKET_NAME


class TrainingPipeline:
    def __init__(self):
        self.traning_pipeline_config = TrainingPipelineConfig()
        self.s3_sync = S3sync()

    def start_data_ingestion(self):
        try:
            self.start_data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.traning_pipeline_config)
            logging.info("Start Data Ingestion Stage")
            data_ingestion = DataIngestion(data_ingestion_config=self.start_data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingestion completed and artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact):
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=self.traning_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config= data_validation_config)
            logging.info("Start Data validation Stage")
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Data validation completed")
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_data_transformation(self ,data_validation_artifact: DataValidationArtifact):
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.traning_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact, data_transformation_config=data_transformation_config)
            logging.info("Start Data Transformation Stage")
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("Data Transformation completed")
            return data_transformation_artifact
             
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            logging.info("Model Training started")
            model_trainer_config = ModelTrainingConfig(self.traning_pipeline_config)
            model_tainer = ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
            model_tainer.initiate_model_trianer()
            logging.info("Model training Completed")

        except Exception as e:
            NetworkSecurityException(e,sys)

    # uploading local arifact to s3 bucket
    def sync_arifact_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.traning_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder=self.traning_pipeline_config.artifact_dir, aws_bucket_url=aws_bucket_url)
        except Exception as e:
            NetworkSecurityException(e, sys)

    # uploading final model to s3 bucket
    def sync_saved_model_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.traning_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder=self.traning_pipeline_config.model_dir, aws_bucket_url=aws_bucket_url)
        except Exception as e:
            NetworkSecurityException(e, sys)

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
            # return model_trainer_artifact
            
            self.sync_arifact_to_s3()
            self.sync_saved_model_dir_to_s3()


        except Exception as e:
            NetworkSecurityException(e,sys) 