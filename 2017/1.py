#!/usr/bin/env python3
import puzzle, library
import re


def one(INPUT):
  total = 0
  INPUT = INPUT[0]
  for pair in zip(INPUT, INPUT[1:] + INPUT[0]):
    if pair[0] == pair[1]: total += int(pair[0])
  return total

def two(INPUT):
  total = 0
  INPUT = INPUT[0]
  mid = len(INPUT) // 2
  for pair in zip(INPUT, INPUT[mid:] + INPUT[:mid]):
    if pair[0] == pair[1]: total += int(pair[0])
  return total

if __name__ == '__main__':
  p = puzzle.Puzzle("2017", "1")

  p.run(one, 0)
  p.run(two, 0)
