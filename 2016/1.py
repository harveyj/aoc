#!/usr/bin/env python3
import puzzle
import re, math
import networkx as nx

def parse(INPUT):
  pat = re.compile('(\w+)+')
  return re.findall(pat, INPUT)

DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))

def one(INPUT, two=True):
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
        return (x, y)
      seen.add((x, y))

  return abs(x) + abs(y)

def two(INPUT):
  return 0

p = puzzle.Puzzle("1")
p.run(one, 0)
