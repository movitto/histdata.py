#!/usr/bin/python3

import os
from common import pandas_data_cols, pandas_data

# Extrapolation Params

FROM = '1m'
TO   = '15m'

FROM_DAY_DIR   = os.path.join(os.getcwd(), "../data/{frm}/daily/".format(frm=FROM))
FROM_MONTH_DIR = os.path.join(os.getcwd(), "../data/{frm}/month/".format(frm=FROM))
FROM_YEAR_DIR  = os.path.join(os.getcwd(),  "../data/{frm}/year/".format(frm=FROM))

TO_DAY_DIR   = os.path.join(os.getcwd(), "../data/{to}/daily/".format(to=TO))
TO_MONTH_DIR = os.path.join(os.getcwd(), "../data/{to}/month/".format(to=TO))
TO_YEAR_DIR  = os.path.join(os.getcwd(),  "../data/{to}/year/".format(to=TO))

# Create required dirs
os.makedirs(TO_DAY_DIR,   exist_ok=True)
os.makedirs(TO_MONTH_DIR, exist_ok=True)
os.makedirs(TO_YEAR_DIR,  exist_ok=True)

ohlc_dict = {
  'Open'      : 'first',
  'High'      : 'max',
  'Low'       : 'min',
  'Close'     : 'last',
  'Volume'    : 'sum',
}

# Extrapolation Helper
def extrapolate(from_dir, to_dir):
  for period in os.listdir(from_dir):
      src  = os.path.join(from_dir, period)
      tgt  = os.path.join(to_dir, period)
      if os.path.exists(tgt):
          continue

      print("Extrapolating ", src, " to ", tgt)
      data = pandas_data(src)
      data.resample(TO.replace("m", "min")).agg(ohlc_dict).to_csv(tgt, columns = pandas_data_cols, index=False)

extrapolate(FROM_DAY_DIR, TO_DAY_DIR)
extrapolate(FROM_MONTH_DIR, TO_MONTH_DIR)
extrapolate(FROM_YEAR_DIR, TO_YEAR_DIR)
