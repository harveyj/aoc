#!/usr/bin/env python3
import puzzle
import itertools, operator

def parse_input(INPUT):
  times = list(map(int, INPUT[0].split()[1:]))
  distances = list(map(int, INPUT[1].split()[1:]))
  return times, distances

def one(INPUT, two=False):
  times, distances = parse_input(INPUT)
  if two:
    times = [int(''.join(map(str, times)))]
    distances = [int(''.join(map(str, distances)))]
  entries = zip(times, distances)
  candidates = []
  for time, distance in entries:
    candidate = 0
    for t in range(time):
      d_travelled = (time - t) * t
      if d_travelled > distance:
        candidate += 1
    candidates.append(candidate)
  return list(itertools.accumulate(candidates, operator.mul))[-1]

def two(INPUT):
  return one(INPUT, two=True)

if __name__ == '__main__':
  p = puzzle.Puzzle("2023", "6")
  p.run(one, 0)
  p.run(two, 0)
