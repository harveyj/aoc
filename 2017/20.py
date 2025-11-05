#!/usr/bin/env python3
import puzzle, library
import re
from collections import defaultdict
from collections import namedtuple

# Step 1: Define the named tuple
Point = namedtuple('Point', ['x', 'y', 'z', 'dx', 'dy', 'dz', 'ax', 'ay', 'az'])

def update(pt, steps=1):
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

def mag(pt):
  return abs(pt.x)+abs(pt.y)+abs(pt.z)

def one(INPUT):
  points = []
  for i, raw in enumerate(parse(INPUT)):
    points.append(Point(*map(int, raw)))
  mag_a = [abs(pt.ax)+abs(pt.ay)+abs(pt.az) for pt in points]
  return mag_a.index(min(mag_a))

def two(INPUT):
  points = []
  for i, raw in enumerate(parse(INPUT)):
    points.append(Point(*map(int, raw)))
  for i in range(1000):
    locs = defaultdict(list)
    new_points = [update(pt) for pt in points]
    for pt in new_points: locs[(pt.x, pt.y, pt.z)].append(pt)
    new_points = [pt for pt in new_points if len(locs[(pt.x, pt.y, pt.z)]) == 1]
    points = new_points
  return len(points)

if __name__ == '__main__':
  p = puzzle.Puzzle("2017", "20")

  p.run(one, 0) 
  p.run(two, 0) 
