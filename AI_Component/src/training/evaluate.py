#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import utils

DATA_PATH = "./data/yahoo_stocks_dataset.txt"
BATCH_SIZE = 128

dataset = utils.StockPriceDataset(DATA_PATH, train_test_split=0.99)
val_dataloader = dataset.validation.to_dataloader(train=False, batch_size=BATCH_SIZE, num_workers=32)

model = utils.StockPriceModel.from_dataset(dataset.training)

print("Start evaluation...")

for _ in range(10):
    begin = time.time()
    output = model.predict(val_dataloader, mode="raw")
    end = time.time()
    print(f"Elapsed time: {end - begin} seconds")

