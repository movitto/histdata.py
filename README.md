# histdata.com utilities

## Intro
Downloads forex data from histdata.com and provides tools to mange groups of data to sample/backtest

### make sync
```make sync```

This will sync data from histdata.com and write it to data/RAW

### make split
```make split```

Split the RAW data into individual years / months / days.
It stores these in data/year, data/month, data/day accordingly

### make groups
```make groups```

Generate randomized groups of data from raw sets (filtered by symbol/year/month/day w/ optional params)
Output json to command line.

## Requirements
The following are required:
* bash
* curl
* sed
* unzip
* Python 3
* Pandas (python library)

## License

Licensed under the MIT license
