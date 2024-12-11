#!/usr/bin/env python3
import puzzle
from collections import deque

def parse(INPUT):
  return [tuple(map(int, l.split(','))) for l in INPUT]

def one(INPUT):
  cubes = parse(INPUT)
  delts = [(-.5, 0, 0),
  (.5, 0, 0), 
  (0, -.5, 0), 
  (0, .5, 0), 
  (0, 0, -.5), 
  (0, 0, .5)]
  seen = set()
  for x, y, z in cubes:
    for dx, dy, dz in delts:
      # print((x+dx, y+dy, z+dz))
      seen.add((x+dx, y+dy, z+dz))
  # print(6*len(cubes) - 2*(6*len(cubes) - len(seen)))
  return 2*len(seen) - 6*len(cubes)

def two(INPUT):
  cubes = parse(INPUT)
  x_max = max([x for x, y, z in cubes]) + 1
  y_max = max([y for x, y, z in cubes]) + 1
  z_max = max([z for x, y, z in cubes]) + 1
  
  def cube_bfs(cubes, x_max, y_max, z_max):
    delts = [(-1, 0, 0),
    (1, 0, 0), 
    (0, -1, 0), 
    (0, 1, 0), 
    (0, 0, -1), 
    (0, 0, 1)]

    queue = deque([(0,0,0)])
    adjacencies = set()
    seen = set()
    while queue:
      node = queue.pop()
      nx, ny, nz = node
      if node in seen: continue
      seen.add(node)
      for dx, dy, dz in delts:
        x, y, z = nx+dx, ny+dy, nz+dz
        if x > x_max or y > y_max or z > z_max or x < -1 or y < -1 or z < -1: continue
        if (x, y, z) in cubes:
          adjacencies.add((node, (x, y, z)))
        else:
          queue.append((x, y, z))
    return len(adjacencies)

  return cube_bfs(cubes, x_max, y_max, z_max)

if __name__ == '__main__':
  p = puzzle.Puzzle("2022", "18")

  p.run(one, 0) 
  p.run(two, 0) 
