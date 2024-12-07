#!/usr/bin/env python3
import puzzle, re
from collections import defaultdict, deque

def parse_input(INPUT):
  def parse_line(l):
    a, b = l.split('~')
    return tuple(map(int, a.split(','))), tuple(map(int, b.split(',')))
  lines = [parse_line(l) for l in INPUT]
  return [(*line, i) for i, line in enumerate(lines)]

def bottom(cube):
  return cube[0][2]  # z2

def one(INPUT):
  def add_brick(supports, brick):
    x1, y1, z1 = brick[0]; x2, y2, z2 = brick[1]; id = brick[2]
    potential_supports = [supports[(x, y)] for x in range(x1, x2+1) for y in range(y1, y2+1)]
    cur_max_z = -1
    supports_for_brick = set()
    for s in potential_supports:
      max_z, support_id = s
      if max_z > cur_max_z:
        supports_for_brick = set([support_id])
        cur_max_z = max_z
      elif max_z == cur_max_z:
        supports_for_brick.add(support_id)
    for x in range(x1, x2+1):
      for y in range(y1, y2+1):
        supports[(x, y)] = (cur_max_z+1+z2-z1, id)
    return supports_for_brick

  bricks = sorted(parse_input(INPUT), key=bottom)
  # supports key: (x, y) val: (max z, id of brick contributing)
  supports = defaultdict(lambda: (0, -1))
  sole_supports = set()
  supports_map = dict()
  for brick in bricks:
    supports_for_brick = add_brick(supports, brick)
    supports_map[brick[2]] = supports_for_brick
    if len(supports_for_brick) == 1 and -1 not in supports_for_brick:
      sole_supports.update(supports_for_brick)
  out2 = 0
  print(supports_map)
  for id in supports_map:
    removed = set([id])
    dirty = True
    while dirty:
      dirty = False
      for id2, deps in supports_map.items():
        if id2 not in removed and len(removed.intersection(deps)) == len(deps):
          # print(' has all deps removed', id2, removed, deps)
          removed.add(id2)
          dirty = True
    out2 += len(removed) - 1
  
  return (len(bricks) - len(sole_supports), out2)

def two(INPUT):
  invals = parse_input(INPUT)
  out = 0
  return out

if __name__ == '__main__':
  p = puzzle.Puzzle("2023", "22")

  p.run(one, 0) 
  p.run(two, 0) 