#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import kafka, time, json, numpy as np

data = {}

topic = "daytrader"
bootstrap_servers = "10.7.19.71:9092"
consumer = kafka.KafkaConsumer(topic, bootstrap_servers=bootstrap_servers, auto_offset_reset="latest")

assert(consumer.bootstrap_connected())
print(f"Bootstrap '{bootstrap_servers}' connected. Listening...")

print(consumer.topics())

messages = []
i = 0

for msg in consumer:
    print(msg)
