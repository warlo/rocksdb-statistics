# rocksdb-statistics

[![PyPI version](https://badge.fury.io/py/rocksdb-statistics.svg)](https://badge.fury.io/py/rocksdb-statistics)

Parses db_bench.log files outputted from RocksDB
Outputs CSV-files and pgfplot of write, compaction and stall statistics.

#### Supported statistics:

- interval_writes
- cumulative_writes
- interval_stall
- cumulative_stall
- interval_compaction
- cumulative_compaction

## Usage

`pip install rocksdb-statistics`

`rocksdb-statistics db_bench.log`
