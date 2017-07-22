#!/usr/bin/python3

import os, sys
import re
import csv
import datetime
import pandas
import calendar

RAW_DIR   = os.path.join(os.getcwd(), "../data/RAW/")
DAY_DIR   = os.path.join(os.getcwd(), "../data/daily/")
MONTH_DIR = os.path.join(os.getcwd(), "../data/month/")
YEAR_DIR  = os.path.join(os.getcwd(), "../data/year/")

# Create required dirs
os.makedirs(DAY_DIR, exist_ok=True)
os.makedirs(MONTH_DIR, exist_ok=True)
os.makedirs(YEAR_DIR, exist_ok=True)

RAW_DATA = {}

# First link existing year / month targets to corresponding dirs
# Also accumuilate raw dirs
for raw in os.listdir(RAW_DIR):
    src_file = os.path.join("../RAW", raw)

    match = re.search(r"([A-Z]+)_([0-9]+).csv", raw)
    sze   = os.stat(os.path.join(RAW_DIR, raw)).st_size
    if match and sze > 0:
        sym   = match.group(1)
        year  = match.group(2)
        month = None

        if sym not in RAW_DATA:
            RAW_DATA[sym] = {}

        if len(year) > 4:
            month = int(year[4:6])
            year  = int(year[0:4])
        else:
            year  = int(year)

        if year not in RAW_DATA[sym]:
            RAW_DATA[sym][year] = []

        if month is not None:
            RAW_DATA[sym][year].append(month)

            tgt_link = os.path.join(MONTH_DIR, raw)
            if not os.path.isfile(tgt_link):
              os.symlink(src_file, tgt_link)

        else:
            tgt_link = os.path.join(YEAR_DIR, raw)
            if not os.path.isfile(tgt_link):
              os.symlink(src_file, tgt_link)

data_cols = ['Symbol', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']

# Helper to extract dataframe via pandas
def pandas_data(fle):
    data = pandas.read_csv(fle, sep=',',
                                header=0,
                                names=data_cols,
                                dtype={'Time':str})

    def conv_time(x):
      return datetime.datetime.strptime(x, "%Y%m%d%H%M")

    data['DateTime'] = data['Time'].apply(conv_time)
    data = data.set_index(pandas.DatetimeIndex(data['DateTime']))

    return data


 Extract individual months out of years
for sym, year_months in RAW_DATA.items():
    for year, months in year_months.items():
        # skip current year
        if year == datetime.datetime.now().year:
            continue

        missing = []
        for m in range(1,13):
            if m not in months:
                missing.append(m)

        if len(missing) > 0:
            print("Missing months", missing, " from ", sym, " year ", year, ", extracting")
            fle = os.path.join(YEAR_DIR, "{sym}_{year}.csv".format(sym=sym, year=year))

            year_data = pandas_data(fle)

            for m in missing:
                pm  = str(m).zfill(2)
                tgt = os.path.join(MONTH_DIR, "{sym}_{year}{month}.csv".format(sym=sym, year=year, month=pm))
                start = "{year}-{month}-1".format(year=year, month=m)
                end   = "{year}-{month}-{day}".format(year=year, month=m, day=calendar.monthrange(year, m)[1])
                year_data.loc[start:end].to_csv(tgt, columns = data_cols, index=False)

# Extract individual days out of months
for mnth in os.listdir(MONTH_DIR):
    print("Splitting {mnth} into days".format(mnth=mnth))

    fle = os.path.join(MONTH_DIR, mnth)
    month_data = pandas_data(fle)

    match      = re.search(r"([A-Z]+)_([0-9]+).csv", mnth)
    sym        = match.group(1)
    year_month = match.group(2)
    month = int(year_month[4:6])
    year  = int(year_month[0:4])
    pm    = str(month).zfill(2)

    days  = calendar.monthrange(year, month)[1]

    for day in range(1, days+1):
        pd=str(day).zfill(2)
        tgt = os.path.join(DAY_DIR, "{sym}_{year}{month}{day}.csv".format(sym=sym, year=year, month=pm, day=pd))

        dte = "{year}-{month}-{day}".format(year=year, month=month, day=day)
        try:
          month_data.loc[dte].to_csv(tgt, columns = data_cols, index=False)

        # ignore error if date is not in data range
        except KeyError:
           pass
