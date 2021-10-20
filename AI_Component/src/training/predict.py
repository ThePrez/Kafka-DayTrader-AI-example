#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

import utils

DATA_PATH = "./data/yahoo_stocks_dataset.txt"
data = pd.read_csv(DATA_PATH, names=["price"])
data["time_idx"] = data.index
data["group"] = 0


dataset = utils.StockPriceDataset(DATA_PATH)
model = utils.StockPriceModel.from_dataset(dataset.training)
model = model.load_from_checkpoint("lightning_logs/version_33_good_one/checkpoints/epoch=19-val_loss=1.93.ckpt")

SIZE = 30
x = pd.DataFrame(dict(
    price=np.array(list(data[:SIZE-6].price) + [0.] * 6),
    group=np.array([0] * SIZE),
    time_idx=np.array(range(SIZE))
    ))
print(x)

print(model.predict(x, mode="prediction"))

