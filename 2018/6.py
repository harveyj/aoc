#!/usr/bin/env python3
import puzzle, re, library
from collections import defaultdict, deque

BUFFER = 1

def one(INPUT):
  coords = list(enumerate([tuple(library.ints(l)) for l in INPUT]))
  coords_x = [c[1][0] for c in coords]
  coords_y = [c[1][1] for c in coords]
  closest = dict()
  infinite = set()
  sx, sy = min(coords_x) - BUFFER, min(coords_y) - BUFFER
  ex, ey = max(coords_x) + BUFFER, max(coords_y) + BUFFER
  for x in range(sx, ex):
    for y in range(sy, ey):
      dists = [(cid, abs(c_loc[0]-x) + abs(c_loc[1] -y)) for cid, c_loc in coords]
      closest[(x, y)] = min(dists, key=lambda a: a[1])[0]

  # print(closest)
  infinite = set(
    [closest[(x, sy)] for x in range(sx, ex)] +
    [closest[(x, ey-1)] for x in range(sx, ex)] + 
    [closest[(sx, y)] for y in range(sy, ey)] +
    [closest[(ex-1, y)] for y in range(sy, ey)])
  # print(infinite)
  counts = [(id, list(closest.values()).count(id)) for id, _ in coords if id not in infinite]
  return max(counts, key=lambda a: a[1])[1]

def two(INPUT):
  coords = list(enumerate([tuple(library.ints(l)) for l in INPUT]))
  coords_x = [c[1][0] for c in coords]
  coords_y = [c[1][1] for c in coords]
  tot_dist = dict()
  sx, sy = min(coords_x) - BUFFER, min(coords_y) - BUFFER
  ex, ey = max(coords_x) + BUFFER, max(coords_y) + BUFFER
  for x in range(sx, ex):
    for y in range(sy, ey):
      tot_dist[(x,y)] = sum([abs(c_loc[0]-x) + abs(c_loc[1] -y) for cid, c_loc in coords])
  
  size = [tot_dist[(x,y)] for x in range(sx, ex) for y in range(sy, ey) if tot_dist[(x, y)] < 10000]
  return len(size)

if __name__ == '__main__':
  p = puzzle.Puzzle("2018", "6")
  print(p.run(one, 0))
  print(p.run(two, 0))