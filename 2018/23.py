#!/usr/bin/env python3
import puzzle, library
from collections import deque

def manhattan(a, b):
  return sum([abs(a[i] - b[i]) for i in range(3)])

def one(INPUT):
  bots = [library.ints(l) for l in INPUT]
  biggest_bot = max(bots, key=lambda b: b[3])
  tot = 0
  for b in bots:
    if manhattan(biggest_bot, b) <= biggest_bot[3]: tot += 1
  return tot

# bounds = x0, y0, z0, x1, y1, z1
def octree(bounds):
  x0, y0, z0, x1, y1, z1 = bounds
  xm = (x0+x1) // 2
  ym = (y0+y1) // 2
  zm = (z0+z1) // 2
  if x0 == xm or y0 == ym or z0 == zm:
    return
  yield x0, y0, z0, xm, ym, zm
  yield x0, y0, zm, xm, ym, z1
  yield x0, ym, z0, xm, y1, zm
  yield x0, ym, zm, xm, y1, z1
  yield xm, y0, z0, x1, ym, zm
  yield xm, y0, zm, x1, ym, z1
  yield xm, ym, z0, x1, y1, zm
  yield xm, ym, zm, x1, y1, z1

def sphere_aabb_intersect(sphere, aabb_min, aabb_max):
    sphere_center = sphere[:3]; sphere_radius = sphere[3]
    cx, cy, cz = sphere_center
    min_x, min_y, min_z = aabb_min
    max_x, max_y, max_z = aabb_max

    # Thanks chatgpt :P
    # Find the closest point on the AABB to the sphere's center
    closest_x = max(min_x, min(cx, max_x))
    closest_y = max(min_y, min(cy, max_y))
    closest_z = max(min_z, min(cz, max_z))
    closest = (closest_x, closest_y, closest_z)

    mnh = manhattan(closest, sphere_center)
    return mnh <= sphere_radius

def size(box):
  return abs((box[3]-box[0]) * (box[4] - box[1]) * (box[5] - box[2]))

def two(INPUT):
  bots = [tuple(library.ints(l)) for l in INPUT]
  mins = [min([b[i] for b in bots]) for i in range(3)]
  maxes = [max([b[i] for b in bots]) for i in range(3)]
  queue = deque([(len(bots), mins+maxes)])
  pts = {(-10000000, -1000000000, -100000000): 0}


  while queue:
    n, box = queue.popleft()
    if size(box) == 1:
      actual_intersected = [b for b in bots if manhattan(box[:3], b[:3]) <= b[3]]
      pts[tuple(box[:3])] = len(actual_intersected)
      continue
    max_val = max(pts.values())
    actual_intersected = [b for b in bots if manhattan(box[:3], b[:3]) <= b[3]]
    if n <= max_val:
      continue
    boxes = octree(box)
    next_boxes = []
    for box in boxes:
      intersected = [b for b in bots if sphere_aabb_intersect(b, box[0:3], box[3:])]
      next_boxes.append((len(intersected), box))
    next_boxes = sorted(next_boxes)
    queue.extendleft(next_boxes)
  max_pts = [sum(key) for key in pts if pts[key] == max_val]
  return min(max_pts)

if __name__ == '__main__':
  p = puzzle.Puzzle("2018", "23")
  print(p.run(one, 0))
  print(p.run(two, 0))