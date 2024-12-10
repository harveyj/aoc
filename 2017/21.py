#!/usr/bin/env python3
import puzzle, library
import re
# import networkx as nx
# import hashlib
# from collections import defaultdict

def all(pat):
  outs = []
  n = len(pat) - 1
  base = [(x, y) for x in range(n+1) for y in range(n+1)]
  out_idxs = [base, 
          [(x, n-y) for (x, y) in base],
          [(n-x, n-y) for (x, y) in base],
          [(n-x, y) for (x, y) in base],
          [(y, x) for (x, y) in base],
          [(n-y, x) for (x, y) in base],
          [(n-y, n-x) for (x, y) in base],
          [(y, n-x) for (x, y) in base],
  ]
  for ox in out_idxs: 
    outs.append([pat[x][y] for x, y in ox])
  return outs

def parse(INPUT):
  patterns = dict()
  for l in INPUT:
    lval, rval = l.split(' => ')
    rows_i = tuple(lval.split('/'))
    rows_o = tuple(rval.split('/'))
    all_i = all(rows_i)
    for row in all_i:
      patterns[tuple(row)] = rows_o
  return patterns

START_PAT = """.#.
..#
###"""

def iter(stride, patterns, G):
  if stride == 2:
    new_G = library.Grid(x=G.max_x() * 3 // 2, y=G.max_y() * 3 // 2)
  else: 
    new_G = library.Grid(x=G.max_x() * 4 // 3, y=G.max_y() * 4 // 3)
  for x in range(0, G.max_x(), stride):
    for y in range(0, G.max_y(), stride):
      key = []
      for dy in range(stride):
        for dx in range(stride):
          key.append(G.get((x+dx, y+dy)))
      out = patterns[tuple(key)]
      sx = x * (stride + 1) // stride
      sy = y * (stride + 1) // stride
      for dy in range(stride+1):
        for dx in range(stride+1):
          new_G.set((sx+dx, sy+dy), out[dy][dx])
  return new_G

def one(INPUT):
  patterns = parse(INPUT)
  G = library.Grid(raw=START_PAT)
  
  steps = 18
  for i in range(steps):
    stride = 2 if G.max_x() % 2 == 0 else 3
    G = iter(stride, patterns, G)
    # print(len(G.detect('#')))
  return 0

# TODO borked
def two(INPUT):
  return 0

if __name__ == '__main__':
  p = puzzle.Puzzle("2017", "21")

  p.run(one, 0) 
  p.run(two, 0) 
