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
max_prediction_length = 6
max_encoder_length = 24

# load dataset
dataset = StockPriceDataset(DATA_PATH)
dl = dataset.training.to_dataloader(train=False, batch_size=1)
x, y = next(iter(dl))

for key in x.keys():
    print(f"##### {key} - {x[key].shape} #####")
    print(x[key])
    print()

# create the model
model = StockPriceModel.from_dataset(dataset.training).load_from_checkpoint(MODEL_PATH)

print(type(model))

print(model.to_onnx("n-beats.onnx", input_sample=x, export_params=True))
#torch.onnx.export(model, random_input, "n-beats.onnx")

