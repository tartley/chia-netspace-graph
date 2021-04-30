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
    return zip(timestamps, values)

def ms_to_secs(rows):
    for ms, value in rows:
        yield ms / 1000, value

def mean(values):
    return sum(values) / len(values)

def window(rows, index, halfsize):
    start = max(0, index - halfsize)
    end = min(len(rows), index + halfsize + 1)
    return [rows[offset] for offset in range(start, end)]

def rolling_average(rows, halfwin=ROLLING_HALFWIN_SIZE):
    rows = list(rows)
    last_col = [row[-1] for row in rows]
    for index, values in enumerate(rows):
        yield *values, mean(window(last_col, index, halfwin))

def growth(rows):
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

def percent_growth(rows):
    for secs, *values, avg, growth in rows:
        if isinstance(avg, float) and isinstance(growth, float):
            percent_growth = growth / avg * 100
        else:
            percent_growth = ""
        yield secs, *values, avg, growth, percent_growth

def print_tsv(rows):
    """Print tab separated values on stdout"""
    for row in rows:
        print("\t".join(str(item) for item in row))

def main():
    print_tsv(
        percent_growth(
            growth(
                rolling_average(
                    ms_to_secs(read_json(sys.stdin)),
                    halfwin=9,
                ),
        ))
    )

if __name__ == "__main__":
    main()


