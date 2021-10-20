#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import kafka
import time
import random
import socketio
import requests
import numpy as np
import json
import pandas as pd
from collections import deque

data = list(pd.read_csv("src/training/data/yahoo_stocks_dataset.txt", names=["price"]).price)
window_size = 128
prices = deque([0.]*window_size, maxlen=window_size)

# for price in data:

#     time.sleep(1.0)



topic = "daytrader"
bootstrap_servers = "10.7.19.71:9092"
producer = kafka.KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda m: json.dumps(m).encode("ascii")
)

assert(producer.bootstrap_connected())
print(f"Bootstrap '{bootstrap_servers}' connected.")

for price in data:
    producer.send("daytrader", {"row": {"price": price}})
    producer.flush()
    time.sleep(0.3)
