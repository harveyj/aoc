#!/usr/bin/env python3
import puzzle, library

def one(INPUT, two=False):
  G = library.Grid(raw='\n'.join(INPUT))
  iters = 1000000 if two else 1
  removed = 0
  while iters > 0:
    locs = set()
    for x in range(G.max_x()):
      for y in range(G.max_y()):
        if G.get((x, y)) == "@" and list(G.neighbors_diag((x, y))).count('@') < 4:
          locs.add((x, y))
          removed += 1
    iters -= 1
    for loc in locs: G.set(loc, '.')
    if not locs: break
  return removed

def two(INPUT):
  return one(INPUT, two=True)

if __name__ == '__main__':
  p = puzzle.Puzzle("2025", "4")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')
