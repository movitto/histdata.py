# histdata.com utilities

## Intro
Downloads forex data from histdata.com and provides tools to mange groups of data to sample/backtest

### make sync
```make sync```

This will sync data from histdata.com and write it to data/1m/year and data/1m/month

### make split
```make split```

Split the 1M data into individual months and days. It stores these in data/1m/month and data/1m/day accordingly

### make extrapolate
```make extrapolate```

Extrapolates higher order timeframes from 1m data. Places these in data/<timeframe>/<period>, eg data/5m/month, data/1H/day, etc

### make groups
```make groups```

Generate randomized groups of data from raw sets (filtered by symbol/year/month/day w/ optional params)

## Conventions

- S = second
- m = minute
- H = hour
- D = day
- W = week
- M = month

5m = 5 minutes ; 3D = 3 days ; 2M = 2 months ; etc

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
