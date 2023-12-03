#!/usr/bin/env python3
import puzzle
import re
import networkx as nx

def one(INPUT):
  seen = set()
  dirs = {'>': (1, 0), '<': (-1, 0), '^': (0, -1), 'v': (0, 1)}
  x, y = 0, 0
  seen.add((x, y))
  for c in INPUT.strip():
    dx, dy = dirs[c]
    x += dx; y += dy
    seen.add((x, y))

  return len(seen)

def two(INPUT):
  seen = set()
  dirs = {'>': (1, 0), '<': (-1, 0), '^': (0, -1), 'v': (0, 1)}
  s_x, s_y = 0, 0
  r_x, r_y = 0, 0
  seen.add((r_x, r_y))
  for i in range(0, len(INPUT), 2):
    s_c = INPUT[i]; r_c = INPUT[i+1]
    s_dx, s_dy = dirs[s_c]
    r_dx, r_dy = dirs[r_c]
    s_x += s_dx; s_y += s_dy
    r_x += r_dx; r_y += r_dy
    seen.add((s_x, s_y))
    seen.add((r_x, r_y))

  return len(seen)

p = puzzle.Puzzle("3")
p.run(one, 0)
p.run(two, 0)
