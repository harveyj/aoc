#!/usr/bin/env python3
import puzzle


PAD = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
DIRS = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}

def one(INPUT):
  x, y = 1, 1
  ret = ''
  for l in INPUT:
    for c in l:
      dx, dy = DIRS[c]
      x += dx; y += dy
      if x < 0: x = 0
      if x > 2: x = 2
      if y < 0: y = 0
      if y > 2: y = 2
    ret += str(PAD[y][x])
  return ret

PAD_TWO = [[0, 0, 1, 0, 0], [0, 2, 3, 4, 0], [5, 6, 7, 8, 9], [0, 'A', 'B', 'C', 0], [0, 0, 'D', 0, 0]]
def two(INPUT):
  x, y = 0, 2
  ret = ''
  for l in INPUT:
    for c in l:
      dx, dy = DIRS[c]
      x += dx; y += dy
      if x < 0 or x > 4 or y < 0 or y > 4 or PAD_TWO[y][x] == 0:
        x -= dx; y -= dy
      # print(x, y)

    ret += str(PAD_TWO[y][x])
  return ret


p = puzzle.Puzzle("2016", "2")
p.run(one, 0)
p.run(two, 0)
