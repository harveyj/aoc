#!/usr/bin/env python3
import puzzle, library

def onetwo(INPUT):
  G = library.Grid(raw='\n'.join(INPUT))
  for x in range(G.max_x()):
    if G.get((x, 0)) != ' ':
      break
  print([len(row) for row in G.grid])
  start = (x, 0)
  dir = (0, 1)
  dir_idx = 0
  x, y = start
  DIRS = ((0, 1), (-1, 0), (0, -1), (1, 0))
  steps = 0
  while True:
    dx, dy = dir
    nx = x + dx; ny = y + dy
    # print('next', nx, ny)
    if G.get((nx, ny), default=' ') in 'ABCDEFGHIJKLNMOPQRSTUVWXYZ':
      print(G.get((nx, ny)))
    if G.get((nx, ny), default = ' ') == ' ':
      # only turn 90 degrees
      tgt_dirs = [1, 3] if dir_idx in [0, 2] else [0, 2]
      for td in tgt_dirs:
        ndx, ndy = DIRS[td]
        new_dir_idx = td
        if G.get((x+ndx, y+ndy), default = ' ') != ' ':
          dir = (ndx, ndy); dir_idx = new_dir_idx
          # print('turning', dir, dir_idx)
          break
      else:
        return steps + 1
    else:
      x, y = nx, ny
      steps += 1
    # print((x, y))
  return 0

def one(INPUT):
  return onetwo(INPUT)
# TODO forgot why this is onetwo
def two(INPUT):
  return 0

if __name__ == '__main__':
  p = puzzle.Puzzle("2017", "19")
  p.run(one, 0)
  p.run(two, 0)