#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
import faust
import json
import time
import requests
from datetime import timedelta
from collections import deque
import socketio


window_size = 24 #128

# connect to the redis queue through Kombu
sio = socketio.KombuManager('amqp://', write_only=True)
print(sio)

prices = deque([0.]*window_size, maxlen=window_size)

if not "KAFKA_BROKER" in os.environ:
    print("Error: 'KAFKA_BROKER' environment variable needs to be defined.")
    sys.exit(1)

app = faust.App(
    "my-app",
    broker=os.environ["KAFKA_BROKER"],
    value_serializer="raw"
)

daytrader_topic = app.topic("daytrader")

last_timestamp = 0
total_messages = 0

@app.agent(daytrader_topic)
async def process(messages):
    global last_timestamp
    global total_messages
    async for msg in messages:
            total_messages += 1
            current_timestamp = int(time.time())
            if current_timestamp > last_timestamp:
                try:
                    prices.append(json.loads(msg)["row"]["price"])
                    last_timestamp = current_timestamp
                except json.decoder.JSONDecodeError:
                    print("Invalid JSON:" + str(msg))


@app.timer(interval=1.0)
async def every_second():
    print(prices)
    print("Last timestamp:", last_timestamp)
    print("Messages count:", total_messages)
    rsp = requests.post("http://127.0.0.1:5000/predict", json={"inputs": list(prices)})

    data = {"price": prices[-1], "predictions": rsp.json()}
    sio.emit("priceData", data)

    print("Prediction:" + str(rsp.json()))

if __name__ == '__main__':

    app.main()
    # run with ./streaming_app.py worker -l info
    # web interface on http://localhost:6066 (see https://faust.readthedocs.io/en/latest/userguide/tasks.html)
    # processing_guarantee

