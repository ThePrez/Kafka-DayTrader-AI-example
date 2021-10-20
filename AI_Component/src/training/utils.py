#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging as log
log.basicConfig(level=log.INFO)

import json
import torch
import pandas as pd
import numpy as np
import pytorch_forecasting as pf
import pytorch_lightning as pl

import warnings
warnings.simplefilter("ignore", UserWarning)
# TODO: temporary fix for "scale is below 1e-7" warning, but we should sort it out


class StockPriceDataset():

    def __init__(self, data_path, train_test_split=0.8):
        prediction_length = 6
        encoder_length = 24

        # load and preprocess data file
        data = pd.read_csv(data_path, names=["price"])
        data["time_idx"] = data.index
        data["group"] = 0

        # split train/val sets
        split_idx = int(data.shape[0] * train_test_split)


        # create TimeSeriesDatasets for training and validation
        self.training = pf.TimeSeriesDataSet(data[:split_idx], 
                            target="price", 
                            time_idx="time_idx", 
                            group_ids=["group"],
                            time_varying_unknown_reals=["price"],
                            min_encoder_length=encoder_length,
                            max_encoder_length=encoder_length,
                            min_prediction_length=prediction_length,
                            max_prediction_length=prediction_length)

        self.validation = pf.TimeSeriesDataSet.from_dataset(self.training, data[split_idx:], 
                            min_prediction_idx=self.training.index.time.max() + 1,
                            stop_randomization=True)


    def __str__(self):
        return json.dumps(self.training.get_parameters(), indent=2, default=str)




class StockPriceModel(pf.NBeats):

    @classmethod
    def from_dataset(cls, dataset):
        return super(StockPriceModel, cls).from_dataset(
            dataset,
            num_blocks=[3, 3],
            num_block_layers=[4, 4],
            widths=[4096, 4096])

