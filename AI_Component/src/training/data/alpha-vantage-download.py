#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import argparse
import logging as log
log.basicConfig(level=log.INFO)

api_key = os.environ["ALPHA_VANTAGE_API_KEY"]
api_endpoint = "https://www.alphavantage.co/query"

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--endpoint", default="TIME_SERIES_DAILY_ADJUSTED",
            help="Endpoint to query. Defaults to 'TIME_SERIES_DAILY_ADJUSTED'")
    parser.add_argument("-s", "--symbol", default="IBM",
            help="Symbol to query. Default to 'IBM'")
    parser.add_argument("-o", "--output", required=True,
            help="(Required) Output file")

    args = parser.parse_args()

    if os.path.exists(args.output):
        raise Exception("Error: path '%s' already exists. Aborting." % args.output)

    params = {
        "function": args.endpoint,
        "symbol": args.symbol,
        "outputsize": "full", 
        "datatype": "csv",
        "apikey": api_key
    }

    rsp = requests.get(api_endpoint, params=params)
    log.info("Request URL: %s" % rsp.url)
    log.info("Status code: %d" % rsp.status_code)

    if rsp.status_code == 200:
        with open(args.output, "w") as f:
            f.write(rsp.text)
            log.info("Data written to '%s'." % args.output)
    else:
        log.error("Status code (%d) is not 200." % rsp.status_code)
        log.error(rsp.content)


