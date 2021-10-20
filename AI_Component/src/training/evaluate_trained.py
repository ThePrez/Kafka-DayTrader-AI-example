#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import logging as log
log.basicConfig(level=log.INFO)
import time
import json

# import torch
import pandas as pd

# import numpy as np
import pytorch_forecasting as pf
import pytorch_lightning as pl
BATCH_SIZE = 128
DATA_PATH = "./data/yahoo_stocks_dataset.txt"

# load and preprocess data
data = pd.read_csv(DATA_PATH, names=["price"])
data["time_idx"] = data.index
data["group"] = 0

# split train/val sets
split_idx = int(data.shape[0] * 0.99)
print(split_idx, data.shape)
max_prediction_length = 6
max_encoder_length = 24

# create DataLoaders
training = pf.TimeSeriesDataSet(data[:split_idx], 
                    target="price", 
                    time_idx="time_idx", 
                    group_ids=["group"],
                    time_varying_unknown_reals=["price"],
                    min_encoder_length=max_encoder_length,
                    max_encoder_length=max_encoder_length,
                    min_prediction_length=max_prediction_length,
                    max_prediction_length=max_prediction_length)

log.info(json.dumps(training.get_parameters(), indent=2, default=str))
validation = pf.TimeSeriesDataSet.from_dataset(training, data[split_idx:], 
                    min_prediction_idx=training.index.time.max() + 1,
                    stop_randomization=True)

train_dataloader = training.to_dataloader(train=True, batch_size=BATCH_SIZE, num_workers=64)
val_dataloader = validation.to_dataloader(train=False, batch_size=BATCH_SIZE, num_workers=64)


begin = time.time()
#model = pf.NBeats.from_dataset(training)
model = pf.NBeats.from_dataset(training, num_blocks=[3, 3], num_block_layers=[4, 4], widths=[4096, 4096])
M = model.load_from_checkpoint("../../checkpoints/nbeats/epoch=19-val_loss=1.93.ckpt")
end = time.time()
log.info(f"Model load time: {end - begin} seconds")

if __name__=="__main__":
    print("Start evaluation...")
    for _ in range(10):
        begin = time.time()
        output = M.predict(val_dataloader, mode="raw")
        end = time.time()
        log.info(f"Elapsed time: {end - begin} seconds")
        # log.info(f"Output shape: {output.shape}")
