import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipeline import SAVED_MODEL_DRI, MODEL_FILE_NAME

class NetworkModel:
    def __init__(self, processor, model):
        try:
            self.preprocessor = processor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def predict(self, x):
        try:
            x_transformed = self.preprocessor.transform(x)
            y_hat = self.model.predict(x)
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e, sys)
