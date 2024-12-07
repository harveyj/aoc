#!/usr/bin/env python3
import puzzle, library

def one(INPUT):
  num = int(INPUT[0])
  total = 2
  incr = 1
  steps = 1
  for _ in range(500):
    incr += 8
    if total <= num < total+incr:
      break
    total += incr
    steps += 1
  incremental = num - total
  octant = incremental // steps
  remainder = incremental % steps
  if octant % 2 == 0:
    return steps + remainder
  else:
    return steps + steps - remainder

VECTORS = [(0, -1), (-1, 0), (0, 1), (1, 0)]
MAX = 100
MID_X = MAX//2
MID_Y = MAX//2
def two(INPUT):
  min_x = MID_X-1; max_x = MID_X+2
  min_y = MID_Y-1; max_y = MID_Y+1
  x = MID_X+1; y = MID_Y
  G = library.Grid(grid=[[0 for i in range(MAX)] for j in range(MAX)])
  G.set((MID_X, MID_Y), 1)
  idx = 0
  while True:
    total = sum(G.neighbors_diag((x, y)))
    G.set((x, y), total)
    if G.get((x, y)) > int(INPUT[0]): return G.get((x, y))
    dx, dy = VECTORS[idx]
    x += dx; y += dy
    if x == min_x:
      min_x -= 1
      idx = (idx + 1) % 4
    if y == min_y:
      min_y -= 1
      idx = (idx + 1) % 4
    if x == max_x:
      max_x += 1
      idx = (idx + 1) % 4
    if y == max_y:
      max_y += 1
      idx = (idx + 1) % 4

if __name__ == '__main__':
  p = puzzle.Puzzle("2017", "3")

  p.run(one, 0)
  p.run(two, 0)
