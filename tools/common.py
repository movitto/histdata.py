import pandas
import datetime

# Data columns to read / write
pandas_data_cols = ['Symbol', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']

# Helper to extract dataframe via pandas
def pandas_data(fle):
    data = pandas.read_csv(fle, sep=',',
                                header=0,
                                names=pandas_data_cols,
                                dtype={'Time':str})

    def conv_time(x):
      return datetime.datetime.strptime(x, "%Y%m%d%H%M")

    data['DateTime'] = data['Time'].apply(conv_time)
    data = data.set_index(pandas.DatetimeIndex(data['DateTime']))

    return data

