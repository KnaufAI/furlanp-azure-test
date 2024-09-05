import os
import logging
import joblib
import json
import numpy as np


def init():
    global model
    model_path = os.path.join(os.getenv("AZUREML_MODEL_DIR"), "model.joblib")
    model = joblib.load(model_path)
    logging.info("init complete")


def run(data):
    logging.info("request received")
    data = json.loads(data)["data"]
    data = np.array(data)
    result = model.predict(data)
    logging.info("request processed")
    return result.tolist()
