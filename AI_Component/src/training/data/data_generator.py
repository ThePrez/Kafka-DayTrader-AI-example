#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from multiprocessing import Pool


GENERATE_PLOTS = False

STOCKS_COUNT = 1

MIN = 120
MAX = 480

def r():
    return np.random.normal(loc=0.0, scale=128.0)

def random_stock(size=86400):
    random_init = np.random.randint(low=MIN+20, high=MAX-20)
    x = np.array([random_init + 0.01 * r(), random_init + 0.01 * r()])
    
    for i in range(size):
        variation = 0.95 * (x[-1] - x[-2]) + 0.01 * r()
        # print(f"Variation: {variation}")
        if not MIN < x[-1] + variation < MAX:
            variation = -variation
        x = np.append(x, x[-1] + variation)

    # x += abs(np.min(x)) + 50 + abs(r())
    return x


def generate_stock(stock_index):
    print(f"Stock {stock_index:03d}")

    # need to re-seed (otherwise all processes
    # would have the same seed)
    np.random.seed()
    values = random_stock(size=86400)

    with open(f"stocks/stock_{stock_index:03d}.txt", "w") as f:
        f.writelines([str(v) + "\n" for v in values])

    if GENERATE_PLOTS:
        pd.Series(values).plot(figsize=(100, 30))
        plt.savefig(f"images/stock_{stock_index:03d}_plot.png")


if __name__=="__main__":

    os.makedirs("stocks/", exist_ok=True)
    if GENERATE_PLOTS:
        os.makedirs("images/", exist_ok=True)

    indexes = list(range(1, STOCKS_COUNT+1))

    with Pool(len(indexes)) as p:
        p.map(generate_stock, indexes)

