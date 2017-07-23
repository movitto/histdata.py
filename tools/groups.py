#!/usr/bin/python3

import os, random

SAMPLE_SIZE   = 50
BACKTEST_SIZE = 25

#DATA_DIR = os.path.join(os.getcwd(), "../data/1m/daily/")
DATA_DIR = os.path.join(os.getcwd(), "../data/1m/month/") # to pull from monthly data pool

print("Sample:")
print(random.sample(os.listdir(DATA_DIR), SAMPLE_SIZE))

print("Backtest:")
print(random.sample(os.listdir(DATA_DIR), BACKTEST_SIZE))
