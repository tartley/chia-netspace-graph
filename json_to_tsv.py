#!/usr/bin/env python3
from dataclasses import dataclass
import json
import math
import sys

# Number of samples rolling average should use on either side of window center
ROLLING_HALFWIN_SIZE = 9

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

def chunk_into_weeks(rows):
    weeks = []
    week = []
    week_start = rows[0].timestamp
    for row in rows:
        while row.timestamp >= (week_start + SECS_PER_WEEK):
            weeks.append(week)
            week = []
            week_start += SECS_PER_WEEK
        week.append(row)
    weeks.append(week)
    return weeks

def calc_growth(rows):
    weeks = chunk_into_weeks(rows)
    result = []
    for weekno, week in enumerate(weeks):
        next_week = weeks[weekno + 1] if weekno + 1 < len(weeks) else None
        # populate growth columns on first row of the week
        if next_week:
            week[0].growth = next_week[0].smooth - week[0].smooth
            week[0].growth_pc = week[0].growth / week[0].smooth * 100
        # copy data for the week
        result.extend(week)
        # insert extra row to draw growth values as flat for the week
        if next_week:
            result.append(
                Datum(
                    next_week[0].timestamp,
                    growth=week[0].growth,
                    growth_pc=week[0].growth_pc,
                )
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
    timestamps = [msec / 1000 for msec in msecs]
    rows = [
        Datum(timestamp=timestamp, raw=raw)
        for timestamp, raw in zip(timestamps, raws)
    ]

    smooths = rolling_average([row.raw for row in rows])
    for smooth, row in zip(smooths, rows):
        row.smooth = smooth

    rows = calc_growth(rows)

    print_tsv(rows)

if __name__ == "__main__":
    main()


