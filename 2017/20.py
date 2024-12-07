#!/usr/bin/env python3
import puzzle, library
import re
import networkx as nx
import hashlib
from collections import defaultdict
from collections import namedtuple

# Step 1: Define the named tuple
Point = namedtuple('Point', ['x', 'y', 'z', 'dx', 'dy', 'dz', 'ax', 'ay', 'az'])

def update(pt):
  dx = pt.dx + pt.ax
  dy = pt.dy + pt.ay
  dz = pt.dz + pt.az
  x = pt.x + dx
  y = pt.y + dy
  z = pt.z + dz
  return Point(x, y, z, dx, dy, dz, pt.ax, pt.ay, pt.az)

def parse(INPUT):
  pat = re.compile('p=<(.+),(.+),(.+)>, v=<(.+),(.+),(.+)>, a=<(.+),(.+),(.+)>')
  for l in INPUT:
    yield re.match(pat, l).groups()

def one(INPUT):
  points = []
  for i, raw in enumerate(parse(INPUT)):
    points.append(Point(*map(int, raw)))
  for i in range(100000):
    # for p in points: print(p)
    new_points = [update(pt) for pt in points]
    new_dists = [abs(pt.x) + abs(pt.y) + abs(pt.z) for pt in new_points]
    print(new_dists.index(min(new_dists)))
    points = new_points
    # print(points)
  return 0

def two(INPUT):
  points = []
  for i, raw in enumerate(parse(INPUT)):
    points.append(Point(*map(int, raw)))
  for i in range(100000):
    locs = defaultdict(list)
    new_points = [update(pt) for pt in points]
    for pt in new_points: locs[(pt.x, pt.y, pt.z)].append(pt)
    new_points = [pt for pt in new_points if len(locs[(pt.x, pt.y, pt.z)]) == 1]
    points = new_points
    print(len(points))
  return 0

if __name__ == '__main__':
  p = puzzle.Puzzle("2017", "20")

  p.run(one, 0) 
  p.run(two, 0) 
