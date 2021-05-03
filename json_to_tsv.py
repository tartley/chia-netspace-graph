#!/usr/bin/env python3
from dataclasses import dataclass
import json
import math
import sys

# Number of samples rolling average should use on either side of window center
ROLLING_HALFWIN_SIZE = 9

# Timestamp at which mainnet launched
# (bodged a bit to match midnight of same day, so growth graph draws lines
# more tidilu aligned with veritical grid), ie:
# Fri Mar 19 2021 00:00:00 GMT-0000
MAINNET_LAUNCH = 1616152620

SECS_PER_WEEK = 60 * 60 * 24 * 7

@dataclass
class Datum:
    timestamp: float
    raw: float = '_'
    smooth: float = '_'
    growth: float = '_'
    growth_pc: float = '_'

def read_json(handle):
    """Read json from stdin"""
    data = json.load(handle)
    values = data["data"]
    timestamps = data["timestamp"]
    assert len(values) == len(timestamps)
    return timestamps, values

def mean(values):
    return sum(values) / len(values)

def window(raws, index, halfsize):
    start = max(-index, -halfsize)
    end = min(halfsize + 1, len(raws) - index)
    return [raws[index + offset] for offset in range(start, end)]

def rolling_average(raws, halfwin=ROLLING_HALFWIN_SIZE):
    return [
        mean(window(raws, index, halfwin))
        for index, values in enumerate(raws)
    ]

def chunk_into_weeks(rows, start):
    weeks = []
    week = []
    week_start = start
    for row in rows:
        while row.timestamp >= (week_start + SECS_PER_WEEK):
            weeks.append(week)
            week = []
            week_start += SECS_PER_WEEK
        week.append(row)
    weeks.append(week)
    return weeks

def calc_growth(rows, start):
    weeks = chunk_into_weeks(rows, start)
    result = []
    week_start = start
    for weekno, week in enumerate(weeks):
        next_week = weeks[weekno + 1] if weekno + 1 < len(weeks) else None
        # insert extra row of growth values at start of the week
        if next_week:
            growth = next_week[0].smooth - week[0].smooth
            growth_pc = growth / week[0].smooth * 100
            result.append(
                Datum(week_start, growth=growth, growth_pc=growth_pc)
            )
        # copy data for the week
        result.extend(week)
        week_start += SECS_PER_WEEK
        # insert extra row at end of week to draw week's growth values as flat
        if next_week:
            result.append(
                Datum(week_start, growth=growth, growth_pc=growth_pc)
            )
    return result

def print_tsv(rows):
    """Print tab separated values on stdout"""
    for row in rows:
        print(
            f"{row.timestamp}\t{row.raw}\t{row.smooth}\t"
            f"{row.growth}\t{row.growth_pc}"
        )

def main():
    msecs, raws = read_json(sys.stdin)
    timestamps = [(msec / 1000) for msec in msecs]
    smooths = rolling_average(raws)
    rows = [
        Datum(timestamp=timestamp, raw=raw, smooth=smooth)
        for timestamp, raw, smooth in zip(timestamps, raws, smooths)
    ]
    rows = calc_growth(rows, MAINNET_LAUNCH)
    print_tsv(rows)

if __name__ == "__main__":
    main()


