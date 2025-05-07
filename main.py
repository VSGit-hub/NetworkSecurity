from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

import sys

if __name__=='__main__':
    try:
        traningpipelieconfig = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(traningpipelieconfig)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info('initiate data ingestion')
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
    except Exception as e:
        raise NetworkSecurityException(e,sys)