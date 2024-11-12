import os
import json
import joblib
import logging
import traceback
import numpy as np


model = None


def init():
    global model
    model_path = os.path.join(os.getenv("AZUREML_MODEL_DIR"), "model.joblib")
    model = joblib.load(model_path)
    logging.info("init complete")


def run(data):
    logging.info("request received")
    data = json.loads(data)

    try:
        data = np.array(data)
        result = model.predict(data)
        logging.info("request processed")
        return result.tolist()
    except Exception as e:
        logging.error("error while processing request")
        print(traceback.format_exc())
        return None