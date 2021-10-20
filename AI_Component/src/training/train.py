#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import pytorch_lightning as pl
import warnings
warnings.simplefilter("ignore", UserWarning)
# TODO: temporary fix for "scale is below 1e-7" warning, but we should sort it out

import utils

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", default="./data/yahoo_stocks_dataset.txt",
            help="Path of stock prices data file")
    parser.add_argument("-b", "--batch_size", type=int, default=128,
            help="Batch size")
    parser.add_argument("-e", "--epochs", type=int, default=20,
            help="Number of epochs")

    args = parser.parse_args()


    dataset = utils.StockPriceDataset(args.data)
    print(dataset)

    train_dataloader = dataset.training.to_dataloader(train=True, batch_size=args.batch_size, num_workers=32)
    val_dataloader = dataset.validation.to_dataloader(train=False, batch_size=args.batch_size, num_workers=32)


    model = utils.StockPriceModel.from_dataset(dataset.training)

    # x, y = next(iter(train_dataloader))
    # for k, v in x.items():
    #     print("---------------", k, "->", v.shape)
    #     print(v)
    # exit()


    # fit the model
    callbacks= [
            pl.callbacks.ProgressBar(refresh_rate=1),
            pl.callbacks.ModelCheckpoint(filename="{epoch}", verbose=True),
            pl.callbacks.LearningRateMonitor(logging_interval="epoch"),
            ]

    trainer = pl.Trainer(max_epochs=args.epochs, gpus=1, callbacks=callbacks)

    trainer.fit(model, 
            train_dataloader=train_dataloader, 
            val_dataloaders=val_dataloader)

# x: dict
#     encoder_cat: encoded categoricals for encoder (long tensor [batch, n_encoder_time_steps, n_features]) 
#     encoder_cont: scaled continuous variables for encoder (float tensor, same size)
#     encoder_target: unscaled continous target or encoded categorical target (float tensor [batch, n_encoder_time_steps])
#     encoder_lengths: lengths of encoder time series
#     decoder_cat:      same for decoder
#     decoder_cont:     same for decoder
#     decoder_target:   same for decoder
#     decoder_lengths:  same for decoder
#     decoder_time_idx: ???
#     groups: encoded group ids to identify a time series
#     target_scale: parameters used to normalize target (mean and standard deviation)
# y: tuple (target, weight)
#     target: unscaled (continous) or encoded (categories) targets
#     weight: ???

# encoder_cat [128, 30, 0]
# encoder_cont [128, 30, 1]
# encoder_target [128, 30]
# encoder_lengths [128]
# decoder_cat [128, 1, 0]
# decoder_cont [128, 1, 1]
# decoder_target [128, 1]
# decoder_lengths [128]
# decoder_time_idx [128, 1]
# groups [128, 1]
# target_scale [128, 2]

