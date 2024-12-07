#!/usr/bin/env python3
import puzzle
import re

def parse(INPUT):
  instrs = [(l.split()[0], int(l.split()[1])) for l in INPUT]
  return instrs

def update_t(hx, hy, tx, ty):
  # print('hx hy tx ty', hx, hy, tx, ty)
  if abs(hx - tx) < 2 and abs(hy - ty) < 2:
    return tx, ty
  if abs(hx - tx) != 0:
    tx += (hx - tx) // abs(hx - tx)
  if abs(hy - ty) != 0:
    ty += (hy - ty) // abs(hy - ty)
  return tx, ty

def one(INPUT):
  START = 10
  instrs = parse(INPUT)
  hx, hy = START, START
  tx, ty = START, START
  tail_locs = set()
  dirs = {'U': [0, -1], 'D': [0, 1], 'L': [-1, 0], 'R': [1, 0]}
  for dir_key, mag in instrs:
    dx, dy = dirs[dir_key]
    for i in range(mag):
      hx += dx; hy += dy
      tx, ty = update_t(hx, hy, tx, ty)
      tail_locs.add((tx, ty))
      # print('\n'.join([''.join(row) for row in grid]))

  return len(tail_locs)

def two(INPUT):
  START = 300
  instrs = parse(INPUT)
  locs = [[START, START] for x in range(10)]
  tail_locs = set()
  dirs = {'U': [0, -1], 'D': [0, 1], 'L': [-1, 0], 'R': [1, 0]}
  for dir_key, mag in instrs:
    dx, dy = dirs[dir_key]
    for i in range(mag):
      # print('step', (dx, dy), i, locs) # step 3 in example is wrong
      locs[0][0] += dx; locs[0][1] += dy
      for j in range(1, 10):
        locs[j] = update_t(locs[j-1][0],locs[j-1][1], locs[j][0], locs[j][1])
      tail = locs[9]
      tail_locs.add(tail)
      # grid = [[" " for i in range(START*2)] for i in range(START*2)]
      # for i in range(10): grid[locs[i][1]][locs[i][0]] = str(i)
      # print('\n'.join([''.join(row) for row in grid]))

  return len(tail_locs)


if __name__ == '__main__':
  p = puzzle.Puzzle("2022", "9")

  p.run(one, 0) 
  p.run(two, 0) 
