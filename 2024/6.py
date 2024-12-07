#!/usr/bin/env python3
import puzzle, re, library
from collections import defaultdict
import copy
import sys

def parse_input(INPUT):
  return INPUT

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def one(INPUT):
  G = library.Grid(raw='\n'.join(INPUT))
  start = G.detect('^')[0]
  dir_idx = 0
  x, y = start
  seen = set()
  while 0 <= x < G.max_x() and 0 <= y < G.max_y():
    seen.add((x, y))
    dx, dy = DIRS[dir_idx]; nx, ny = x+dx, y+dy
    if G.get((nx, ny)) == '#':
      dir_idx = (dir_idx + 1) % 4
      continue
    x, y = nx, ny
  return len(seen)


def two(INPUT):
  def find_loop(G, seen, dir_idx, x, y):
    # print('.', end=''); sys.stdout.flush()
    new_seen = set()
    new_G = library.Grid(grid=G.grid)
    dx, dy = DIRS[dir_idx]; nx, ny = x+dx, y+dy
    if 0 <= nx < G.max_x() and 0 <= ny < G.max_y():
      if (nx, ny) in [s[0] for s in seen]:
        print('WOULD BLOCK PRIOR PATH')
        return [], None
      else:
        new_G.set((nx, ny), '#')
        new_block = (nx, ny)
    else:
      return [], None
    while 0 <= x < new_G.max_x() and 0 <= y < new_G.max_y():
      # print((x, y)); sys.stdout.flush()
      if ((x, y), DIRS[dir_idx]) in new_seen:
        return list(new_seen), new_block
      new_seen.add(((x, y), DIRS[dir_idx]))
      dx, dy = DIRS[dir_idx]; nx, ny = x+dx, y+dy
      if new_G.get((nx, ny)) == '#':
        dir_idx = (dir_idx + 1) % 4
        continue
      x, y = nx, ny
    return [], None
  G = library.Grid(raw='\n'.join(INPUT))
  start = G.detect('^')[0]
  dir_idx = 0
  x, y = start
  seen = set()
  obstructions = set()
  # print(G)
  while 0 <= x < G.max_x() and 0 <= y < G.max_y():
    seen.add(((x, y), DIRS[dir_idx]))
    dx, dy = DIRS[dir_idx]; nx, ny = x+dx, y+dy
    # print((x, y), (nx, ny), G.get((nx, ny)))
    # print(G, end='\n\n')
    # input()
    # sys.stdout.flush()
    if G.get((nx, ny)) == '#':
      dir_idx = (dir_idx + 1) % 4
      continue
    loop, new_block = find_loop(G, seen, dir_idx, x, y)

    if loop:
      obstructions.add(new_block)
      G.overlays = {pt[0]:'L' for pt in loop}
      G.overlays[new_block] = 'O'; G.overlays[start] = '^'
      # print(G); input()
      # print(loop)
      G.overlays = {}
    x, y = nx, ny
  return len(obstructions)

# not 2212, 2038
if __name__ == '__main__':
  p = puzzle.Puzzle("2024", "6")

  p.run(one, 0)
  p.run(two, 0)
