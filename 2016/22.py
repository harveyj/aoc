#!/usr/bin/env python3
import puzzle, library
import re
import networkx as nx
import hashlib


def parse(INPUT):
  pat = re.compile('/dev/grid/node-x(\d+)-y(\d+)\s*(\d+)T\s*(\d+)T\s*(\d+)T.*')
  for l in INPUT:
    yield re.match(pat, l).groups()


def one(INPUT):
  cells = dict()
  for l in parse(INPUT):
    x, y, total, used, avail = list(map(int, l))
    # print(x, y, total, used, avail)
    cells[(x,y)] = (total, used, avail)
  print(cells)
  legal = set()
  for x in range(38):
    for y in range(28):
      for x2 in range(38):
        for y2 in range(28):
          if x == x2 and y == y2:
            continue
          if cells[(x, y)][1] == 0:
            continue
          if cells[(x, y)][1] < cells[(x2, y2)][2]:
            legal.add(((x, y), (x2, y2)))
  return len(legal)

def two(INPUT):
  cells = dict()
  for l in parse(INPUT):
    x, y, total, used, avail = list(map(int, l))
    # print(x, y, total, used, avail)
    cells[(x,y)] = (total, used, avail)
  print(cells[37, 0])
  max_x = 38
  max_y = 28
  G = library.Grid(x=max_x, y=max_y)
  for x in range(38):
    for y in range(28):
      total, used, avail = cells[(x, y)]
      if used <= 89:
        print('could be used', (x, y))
        G.set((x, y), '#')
      if avail > 70:
        print('blank cell', (x, y), avail)
        G.set((x, y), '@')

  print(G)

p = puzzle.Puzzle("22")
# p.run(one, 0)
p.run(two, 0)
