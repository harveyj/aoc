#!/usr/bin/env python3
import puzzle
import itertools, operator
def parse_input(INPUT):
  times = list(map(int, INPUT[0].split()[1:]))
  distances = list(map(int, INPUT[1].split()[1:]))
  return times, distances

def one(INPUT):
  times, distances = parse_input(INPUT)
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


# input 3 is the hand-edited input for part 2
if __name__ == '__main__':
  p = puzzle.Puzzle("2023", "6")
  p.run(one, 0)
  p.run(one, 3)
