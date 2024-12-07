#!/usr/bin/env python3
import puzzle
import re

def parse(INPUT):
  pat = re.compile('(\d+)-(\d+)')
  for l in INPUT:
    yield list(map(int, re.match(pat, l).groups()))

def one(INPUT, max=4294967295):
  ranges = list(parse(INPUT))
  events = []
  for r in ranges:
    events.append((r[0], 's', r[1]))
    events.append((r[1], 'e', r[0]))
  events.append((max+1, 's', None))
  events.append((max+2, 'END', None))
  events = sorted(events)
  depth = 0
  zero_ranges = []
  last_zero_start = 0
  for e, next in zip(events, events[1:]):
    loc, code, other = e
    if code == 's':
      if depth == 0:
        zero_ranges.append((last_zero_start, loc))
      depth += 1
    else:
      depth -= 1
      if depth == 0 and next[0] > loc:
        last_zero_start = loc+1
  # zero_ranges.append((last_zero_start, max))
  zero_ranges = [(s, e) for (s, e) in zero_ranges if s != e]
  # print('zr',zero_ranges)
  return zero_ranges[0][0]

def two(INPUT, end_range=4294967295):
  ranges = list(parse(INPUT))
  events = []
  for r in ranges:
    events.append((r[0], 's', r[1]))
    events.append((r[1], 'e', r[0]))
  # dummy event to terminate the end of the legal range
  events.append((end_range, 's', end_range+1))
  events = sorted(events)
  zero_ranges = []
  max_last = 0
  for e in events:
    loc, code, other = e
    if code == 's':
      # print(loc, max_last)
      if loc > max_last:
        zero_ranges.append((max_last+1, loc))
      max_last = max(max_last, other)
    # print(loc, max_last)

  # zero_ranges.append((last_zero_start, max))
  zero_ranges = [(s, e) for (s, e) in zero_ranges if s != e]
  # print('zr',zero_ranges)
  zero_mags = [e - s for s, e in zero_ranges]
  return sum(zero_mags)

if __name__ == '__main__':
  p = puzzle.Puzzle("2016", "20")

  p.run(one, 0)
  p.run(two, 0)
