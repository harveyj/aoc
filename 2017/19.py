#!/usr/bin/env python3
import puzzle, library

def onetwo(INPUT):
  G = library.Grid(raw='\n'.join(INPUT))
  for x in range(G.max_x()):
    if G.get((x, 0)) != ' ':
      break
  start = (x, 0)
  dir = (0, 1)
  dir_idx = 0
  x, y = start
  DIRS = ((0, 1), (-1, 0), (0, -1), (1, 0))
  steps = 0
  outs = []
  while True:
    dx, dy = dir
    nx = x + dx; ny = y + dy
    if G.get((nx, ny), default=' ') in 'ABCDEFGHIJKLNMOPQRSTUVWXYZ':
      outs.append(G.get((nx, ny)))
    if G.get((nx, ny), default = ' ') == ' ':
      # only turn 90 degrees
      tgt_dirs = [1, 3] if dir_idx in [0, 2] else [0, 2]
      for td in tgt_dirs:
        ndx, ndy = DIRS[td]
        new_dir_idx = td
        if G.get((x+ndx, y+ndy), default = ' ') != ' ':
          dir = (ndx, ndy); dir_idx = new_dir_idx
          break
      else:
        return ''.join(outs), steps + 1
    else:
      x, y = nx, ny
      steps += 1

def one(INPUT):
  return onetwo(INPUT)[0]

def two(INPUT):
  return onetwo(INPUT)[1]

if __name__ == '__main__':
  p = puzzle.Puzzle("2017", "19")
  p.run(one, 0)
  p.run(two, 0)