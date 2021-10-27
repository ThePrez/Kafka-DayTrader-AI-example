#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import onnxruntime as ort
import time
from flask import Flask, request
import numpy as np


MODEL_PATH = "./n-beats.onnx"



# create ONNXRuntime session and load model
ort_session = ort.InferenceSession(MODEL_PATH)

# Create Flask app
app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def predict():

    inputs = np.array(request.json["inputs"])

    # normalize input
    inputs_mean, inputs_std = np.mean(inputs), np.std(inputs)
    normalized_inputs = (inputs - inputs_mean) / inputs_std

    inputs = {
        ort_session.get_inputs()[0].name: np.reshape(normalized_inputs, (1, 24, 1)).astype(np.float32),
        ort_session.get_inputs()[1].name: np.array([[inputs_mean, inputs_std]]).astype(np.float32)
    }

    start = time.perf_counter()
    predicted = ort_session.run(None, inputs)
    duration = time.perf_counter() - start

    print(f"Predicted: {predicted[0]}")
    print(f"Inference duration: {duration}s")
    return str(np.nan_to_num(predicted[0][0]).tolist())


if __name__=="__main__":
    app.run(host="0.0.0.0")
