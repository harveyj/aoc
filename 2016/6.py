#!/usr/bin/env python3
import puzzle
from collections import defaultdict

def puzz(lines, two=False):
  width = len(lines[0])
  hist = [defaultdict(int) for i in range(width)]
  for l in lines:
    for i, c in enumerate(l):
      hist[i][c] += 1
  out = []
  for i in range(width):
    items = hist[i].items()
    max_item = sorted(items, key=lambda a: a[1])[-1]
    if two: max_item = sorted(items, key=lambda a: a[1])[0]
    out.append(max_item[0])
  return ''.join(out)

def one(INPUT):
  return puzz(INPUT)

def two(INPUT):
  return puzz(INPUT, two=True)

p = puzzle.Puzzle("2016", "6")
p.run(one, 0)
p.run(two, 0)
