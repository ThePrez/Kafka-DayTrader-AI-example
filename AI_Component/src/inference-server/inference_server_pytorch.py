#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import time
from flask import Flask, request
import numpy as np
import pandas as pd
import pytorch_forecasting as pf

from utils import StockPriceDataset, StockPriceModel

MODEL_PATH = "./n-beats.ckpt"
DATA_PATH = "../training/data/yahoo_stocks_dataset.txt"

# load and preprocess data
data = pd.read_csv(DATA_PATH, names=["price"])
data["time_idx"] = data.index
data["group"] = 0

# split train/val sets
split_idx = int(data.shape[0] * 0.8)

max_prediction_length = 6
max_encoder_length = 24

# load dataset
dataset = StockPriceDataset(DATA_PATH)

# create the model
model = StockPriceModel.from_dataset(dataset.training).load_from_checkpoint(MODEL_PATH)


# Create Flask app
app = Flask(__name__)

SIZE = max_prediction_length + max_encoder_length
default_group = np.array([0] * SIZE)
default_timeidx = np.array(range(SIZE))

@app.route("/predict", methods=["POST"])
def predict():

    input_seq = pd.DataFrame({
        "price": np.array(request.json["inputs"] + [0.] * max_prediction_length),
        "group": default_group,
        "time_idx": default_timeidx
    })

    start = time.perf_counter()
    predicted = model.predict(input_seq)
    duration = time.perf_counter() - start

    print("Predicted:", np.array(predicted))
    print(f"Inference duration: {duration}s")
    return str(predicted[0].tolist())



if __name__=="__main__":
    app.run()
