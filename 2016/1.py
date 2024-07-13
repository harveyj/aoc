#!/usr/bin/env python3
import puzzle
import re, math
import networkx as nx

def parse(INPUT):
  pat = re.compile('(\w+)+')
  return re.findall(pat, INPUT[0])

DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))

def puzz(INPUT, two=False):
  dir_idx = 0
  x, y = 0, 0
  seen = set()
  for move in list(parse(INPUT)):
    # print(move)
    dir_idx += 1 if move[0] == 'R' else -1
    dx, dy = DIRS[dir_idx % 4]
    mag = int(move[1:])
    for i in range(mag):
      x += dx; y += dy
      if (x, y) in seen and two:
        return abs(x)+abs(y)
      seen.add((x, y))

  return abs(x) + abs(y)

def one(INPUT):
  return puzz(INPUT)

def two(INPUT):
  return puzz(INPUT, two=True)

p = puzzle.Puzzle("2016", "1")
p.run(one, 0)
p.run(two, 0)
