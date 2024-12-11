#!/usr/bin/env python3
import puzzle, re, library
from collections import deque

def parse_input(INPUT):
  return library.Grid(raw='\n'.join(INPUT))

def fslash(dir):
  return -dir[1], -dir[0]

def bslash(dir):
  return dir[1], dir[0]

def solve(start, dir, G):
  # loc, (dx, dy)
  queue = deque([(start, dir)])
  locs = set()
  seen = set()
  while queue:
    loc, dir = queue.pop()
    locs.add(loc)
    if (loc, dir) in seen: continue
    seen.add((loc, dir))
    # G.overlays[loc] = 'X'
    new_loc = library.pt_add(loc, dir)
    cell = G.get(new_loc)
    if cell == '.':
      queue.append((new_loc, dir))
    elif cell == '|':
      if dir[0]:
        queue.append((new_loc, (0, -1)))
        queue.append((new_loc, (0, 1)))
      else: 
        queue.append((new_loc, dir))
    elif cell == '-':
      if dir[1]:
        queue.append((new_loc, (-1, 0)))
        queue.append((new_loc, (1, 0)))
      else: 
        queue.append((new_loc, dir))
    elif cell == '/':
      queue.append((new_loc, fslash(dir)))
    elif cell == '\\':
      queue.append((new_loc, bslash(dir)))
    # out of bounds returns '#' which we treat like a wall
  # print(G)
  # first location is technically invalid
  return len(locs) - 1 

def one(INPUT):
  G = parse_input(INPUT)
  return solve((-1, 0), (1, 0), G)

def two(INPUT):
  G = parse_input(INPUT)
  tiles = dict()
  for x in range(G.max_x()):
    tiles[(x, 0)] = solve((x, -1), (0, 1), G)
    tiles[(x, G.max_y())] = solve((x, G.max_y() + 1), (0, -1), G)
  for y in range(G.max_y()):
    tiles[(0, y)] = solve((-1, y), (1, 0), G)
    tiles[(G.max_x(), y)] = solve((y, G.max_x() + 1), (-1, 0), G)
  # for k in tiles:
  #   print(k, tiles[k])
  return max(tiles.values())

if __name__ == '__main__':
  p = puzzle.Puzzle("2023", "16")

  p.run(one, 0) 
  p.run(two, 0) 
