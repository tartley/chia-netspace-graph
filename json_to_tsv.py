#!/usr/bin/env python3
import json
import math
import sys

# Number of samples rolling average should use, before and after offset=0
ROLLING_HALFWIN_SIZE = 9

SECS_PER_WEEK = 60 * 60 * 24 * 7

def read_json(handle):
    """Read json from stdin"""
    data = json.load(handle)
    values = data["data"]
    timestamps = data["timestamp"]
    assert len(values) == len(timestamps)
    return timestamps, values

###

def growth_old(rows):
    last_secs = None
    last_avg = None
    for secs, *values, avg in rows:
        if last_secs and last_avg:
            growth_per_sec = (avg - last_avg) / (secs - last_secs)
            growth = growth_per_sec * SECS_PER_WEEK
        else:
            growth = ""
        last_secs = secs
        last_avg = avg
        yield secs, *values, avg, growth

def percent_growth_old(rows):
    for secs, *values, avg, growth in rows:
        if isinstance(avg, float) and isinstance(growth, float):
            percent_growth = growth / avg * 100
        else:
            percent_growth = ""
        yield secs, *values, avg, growth, percent_growth

###

def mean(values):
    return sum(values) / len(values)

def window(raws, index, halfsize):
    start = max(0, index - halfsize)
    end = min(len(raws), index + halfsize + 1)
    return [raws[offset] for offset in range(start, end)]

def rolling_average(raws, halfwin=ROLLING_HALFWIN_SIZE):
    return [
        mean(window(raws, index, halfwin))
        for index, values in enumerate(raws)
    ]

def print_tsv(*cols):
    """Print tab separated values on stdout"""
    for row in zip(*cols):
        print("\t".join(str(item) for item in row))

def main():
    msecs, raws = read_json(sys.stdin)
    secs = [msec / 1000 for msec in msecs]
    smooths = rolling_average(raws)
    print_tsv(secs, raws, smooths)

if __name__ == "__main__":
    main()


