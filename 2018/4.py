#!/usr/bin/env python3
import puzzle
from collections import defaultdict

def one(INPUT):
  timestamps = sorted(INPUT)
  minutes = defaultdict(lambda: defaultdict(int))
  i = 0
  while i < len(timestamps):
    id_line = timestamps[i]
    id = id_line.split('#')[1].split()[0]
    i += 1
    while i < len(timestamps) and '#' not in timestamps[i]:
      s = int(timestamps[i].split(':')[1].split(']')[0])
      e = int(timestamps[i+1].split(':')[1].split(']')[0])
      for j in range(s, e):
        minutes[id][j] += 1
      i += 2
  max_guard = max(minutes, key=lambda a: sum(minutes[a].values()))
  max_min = max(minutes[max_guard], key=lambda a: minutes[max_guard][a])
  return int(max_guard) * max_min

def two(INPUT):
  timestamps = sorted(INPUT)
  minutes = defaultdict(lambda: defaultdict(int))
  i = 0
  while i < len(timestamps):
    id_line = timestamps[i]
    id = id_line.split('#')[1].split()[0]
    i += 1
    while i < len(timestamps) and '#' not in timestamps[i]:
      s = int(timestamps[i].split(':')[1].split(']')[0])
      e = int(timestamps[i+1].split(':')[1].split(']')[0])
      for j in range(s, e):
        minutes[id][j] += 1
      i += 2
  max_sleeps = 0
  max_guard_id = 0
  max_minute_id = 0
  for guard in minutes:
    max_min = max(minutes[guard], key=lambda a: minutes[guard][a])
    if minutes[guard][max_min] > max_sleeps:
      max_guard_id = guard
      max_minute_id = max_min
      max_sleeps = minutes[guard][max_min]

  return int(max_guard_id) * max_minute_id

if __name__ == '__main__':
  p = puzzle.Puzzle("2018", "4")

  # print(p.run(one, 0))
  print(p.run(two, 0))
