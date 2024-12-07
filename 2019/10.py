#!/usr/bin/env python3
import puzzle
import math
from itertools import chain

def one(INPUT):
  pts = []

  for i, l in enumerate(INPUT):
    for j, k in enumerate(l):
      if k == '#':
        pts.append((j, i))

  max_angles = 0
  for pt1 in pts:
    angles = []
    for pt2 in pts:
      if pt1 == pt2: continue
      angle = math.atan2((pt1[1]-pt2[1]), (pt1[0] - pt2[0]))
      if angle not in angles:
        angles.append(angle)
    if len(angles) > max_angles:
      max_angles = len(angles)
  return max_angles

def two(INPUT):
  pts = []
  grid = [['.' for i in range(len(INPUT[0]))] for j in range(len(INPUT))]

  for i, l in enumerate(INPUT):
    for j, k in enumerate(l):
      if k == '#':
        pts.append((j, i))
        grid[i][j] = '#'

  def find_closest(pt1, ptarray):
    closest = ptarray[0]
    for p in ptarray:
      min_dist = abs(closest[0] - pt1[0]) + abs(closest[1] - pt1[1])
      cur_dist = abs(p[0] - pt1[0]) + abs(p[1] - pt1[1])
      if min_dist < cur_dist:
        closest = p

    return p

  pt1 = (20, 19)
  # pt1 = (11, 13)
  # # pt1 = (8, 3)

  grid[pt1[1]][pt1[0]] = "X"
  angles_to_points = {}
  for pt2 in pts:
    if pt1 == pt2: continue
    angle = math.atan2((pt1[0]-pt2[0]), (pt1[1] - pt2[1]))
    points = angles_to_points.get(angle, [])
    points.append(pt2)
    angles_to_points[angle] = points

  angles = list(angles_to_points.keys())
  angles.sort()
  angles.reverse()
  i = 0
  while angles[i] > 0:
    i += 1
  angles = angles[i:] + angles[:i]

  num_destroyed = 0
  for i, angle in chain(enumerate(angles), enumerate(angles)):
    num_destroyed += 1
    closest = find_closest(pt1, angles_to_points[angle])
    angles_to_points[angle].remove(closest)
    grid[closest[1]][closest[0]] = str(i)
    if num_destroyed == 200:
      return closest[0] * 100 + closest[1]

if __name__ == '__main__':
  p = puzzle.Puzzle("2019", "10")

  p.run(one, 0)
  p.run(two, 0)
