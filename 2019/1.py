#!/usr/bin/env python3
import puzzle

def parse_input(INPUT):
  return INPUT

def one(INPUT):
  invals = parse_input(INPUT)
  tot = 0
  for val in invals:
    tot += int(val) // 3 - 2
  return tot

def two(INPUT):
  invals = parse_input(INPUT)
  tot = 0
  l = 1969
  inc = int(l) // 3 - 2
  while inc > 0:
    tot += inc
    inc = inc / 3 - 2

  tot = 0
  for l in invals:
    inc = int(l) // 3 - 2
    while inc > 0:
      tot += inc
      inc = inc // 3 - 2
  return tot

if __name__ == '__main__':
  p = puzzle.Puzzle("2019", "1")

  p.run(one, 0)
  p.run(two, 0)
