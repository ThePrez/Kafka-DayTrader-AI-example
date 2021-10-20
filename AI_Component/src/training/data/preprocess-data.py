#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import glob
import random
import os

import matplotlib.pyplot as plt

# set to True to generate individual plots for each stock
GENERATE_PLOTS = False 


if GENERATE_PLOTS:
    os.makedirs("images/", exist_ok=True)

# get paths of all CSVs
csv_paths = sorted(glob.glob("./yahoo_stocks/*.csv"))

# init Series of aggregated plots
prices = pd.Series([1.0,])

for csv in csv_paths:
    new = pd.read_csv(csv, usecols=["Close"]).Close

    if GENERATE_PLOTS:
        new.plot()
        plt.savefig(f"images/{os.path.basename(csv)[:-4]}.png")
        plt.clf()

    # ensure junction with previous plot
    new = new + prices.iloc[-1] - new.iloc[0]

    # concatenate to existing prices list
    prices = pd.concat([prices, new], ignore_index=True)

# add further normalization (to avoid negative prices)
prices = prices + 50

# apply rolling window to flatten a bit
prices = prices.rolling(10).mean().dropna()

print(f"Total elements: {len(prices)}")
print(f"Price range: [{prices.min()}, {prices.max()}]") 


if GENERATE_PLOTS:
    prices.plot()
    plt.savefig("images/yahoo_stocks_dataset.png")

with open("yahoo_stocks_dataset.txt", "w") as f:
    f.writelines([str(e) + "\n" for e in prices.to_list()])

