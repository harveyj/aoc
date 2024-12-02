#!/usr/bin/env python3
import puzzle, re

def parse_input(INPUT):
  for l in INPUT:
    yield list(map(int, l.split()))

def one(INPUT):
  raw = list(parse_input(INPUT))
  a = [item[0] for item in raw]
  b = [item[1] for item in raw]
  a.sort()
  b.sort()
  totals = [abs(i - j) for i, j in zip(a, b)]
  return sum(totals)

def two(INPUT):
  raw = list(parse_input(INPUT))
  a = [item[0] for item in raw]
  b = [item[1] for item in raw]
  totals = [i * b.count(i) for i in a]
  return sum(totals)

p = puzzle.Puzzle("2024", "1")
p.run(one, 0)
p.run(two, 0)
