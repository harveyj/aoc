#!/usr/bin/env python3
import puzzle, library
import re


def parse(INPUT):
  for l in INPUT:
    yield list(map(int, l.split()))


def one(INPUT):
  total = 0
  for l in parse(INPUT):
    total += max(l) - min(l)
  return total

def two(INPUT):
  total = 0
  for l in parse(INPUT):
    for i in range(len(l)):
      for j in range(len(l)):
        if i != j and l[i] % l[j] == 0:
          total += l[i] // l[j]
  return total

if __name__ == '__main__':
  p = puzzle.Puzzle("2017", "2")

  p.run(one, 0)
  p.run(two, 0)
