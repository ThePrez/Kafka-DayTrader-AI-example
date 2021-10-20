#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import random
import socketio
import requests

import pandas as pd
from collections import deque

# connect to the redis queue through Kombu
sio = socketio.KombuManager('amqp://', write_only=True)
print(sio)

def r():
    return random.uniform(50, 80)

data = list(pd.read_csv("../../yahoo_stocks_dataset.txt", names=["price"]).price)
window_size = 128
prices = deque([0.]*window_size, maxlen=window_size)

for price in data:
    prices.append(price)
    last_prices = [prices[x] for x in range(len(prices) - 30, len(prices))]
    rsp = requests.post("http://127.0.0.1:5000/predict", json={"inputs": last_prices})
    data = {"price": price, "predictions": rsp.json()}
    sio.emit("priceData", data)
    print(".", end="", flush=True)
    # time.sleep(1.0)
    time.sleep(0.3)




# while True:
#     data = {"price": r(), "predictions": [r() for _ in range(6)]}
#     sio.emit("priceData", data)
#     print(".", end="", flush=True)
#     time.sleep(1.0)
