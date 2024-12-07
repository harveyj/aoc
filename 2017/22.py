#!/usr/bin/env python3
import puzzle, library

def one(INPUT):
  in_lines = INPUT
  MAX_X = 500; MAX_Y = 500
  G = library.Grid(x=MAX_X, y=MAX_Y)
  center_x = MAX_X // 2; center_y = MAX_Y // 2
  pat_start_x = center_x - len(in_lines[0]) // 2
  pat_start_y = center_y - len(in_lines) // 2
  
  for dx in range(len(in_lines[0])):
    for dy in range(len(in_lines)):
      G.set((pat_start_x + dx, pat_start_y + dy), in_lines[dy][dx])
  pt = (center_x, center_y)
  DIRS = ((0, -1), (1, 0), (0, 1), (-1, 0))
  dir_idx = 0
  bursts = 0
  for i in range(10000):
    if G.get(pt) == '#':
      dir_idx = (dir_idx + 1) % 4
      G.set(pt, '.')
    else:
      dir_idx = (dir_idx + 3) % 4
      G.set(pt, '#')
      bursts += 1
    dx, dy = DIRS[dir_idx]
    pt = pt[0] + dx, pt[1] + dy
    G.overlays = {pt: '@'}
  return bursts

def two(INPUT):
  in_lines = INPUT
  MAX_X = 15000; MAX_Y = 15000
  G = library.Grid(x=MAX_X, y=MAX_Y)
  center_x = MAX_X // 2; center_y = MAX_Y // 2
  pat_start_x = center_x - len(in_lines[0]) // 2
  pat_start_y = center_y - len(in_lines) // 2
  
  for dx in range(len(in_lines[0])):
    for dy in range(len(in_lines)):
      G.set((pat_start_x + dx, pat_start_y + dy), in_lines[dy][dx])
  pt = (center_x, center_y)
  DIRS = ((0, -1), (1, 0), (0, 1), (-1, 0))
  dir_idx = 0
  bursts = 0
  for i in range(10000000):
    if G.get(pt) == '#':
      dir_idx = (dir_idx + 1) % 4
      G.set(pt, 'F')
    elif G.get(pt) == 'W':
      G.set(pt, '#')
      bursts += 1
    elif G.get(pt) == 'F':
      dir_idx = (dir_idx + 2) % 4
      G.set(pt, '.')
    elif G.get(pt) == '.':
      dir_idx = (dir_idx + 3) % 4
      G.set(pt, 'W')
    dx, dy = DIRS[dir_idx]
    pt = pt[0] + dx, pt[1] + dy
    G.overlays = {pt: '@'}
    # print(G)
    # input()
  return bursts

if __name__ == '__main__':
  p = puzzle.Puzzle("2017", "22")

  p.run(one, 0)
  p.run(two, 0)
