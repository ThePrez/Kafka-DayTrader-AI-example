#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas_datareader as pdr
import datetime as dt

with open("stocks.txt", "r") as f:
    stocks = f.read().splitlines()

start = dt.datetime(1990,1,1)
end   = dt.datetime(2020,1,1)
start_str = start.strftime("%d%m%Y")
end_str   = end.strftime("%d%m%Y")

out_dir = "yahoo_stocks" 
os.makedirs(out_dir, exist_ok=True)

for i, stock in enumerate(stocks):
    print(f"[{i+1}/{len(stocks)}] {stock}")
    out_name = f"{out_dir}/{stock}_{start_str}_{end_str}.csv"
    if os.path.isfile(out_name):
        print(f"File '{out_name}' exists, skipping.")
    else:
        try:
            pdr.DataReader(stock, "yahoo", start, end).to_csv(out_name)
            print(f"File '{out_name}' written.")
        except Exception as e:
            print(repr(e))

