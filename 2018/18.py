#!/usr/bin/env python3
import puzzle, library

def parse_input(INPUT):
  return library.Grid(raw='\n'.join(INPUT))

def all_grids(G):
  i = 0
  while True:
    new_G = library.Grid(grid=G.grid)
    for x in range(G.max_x()):
      for y in range(G.max_y()):
        c = G.get((x, y))
        neigh = list(G.neighbors_diag((x, y)))
        if c == '.' and neigh.count('|') >= 3: new_G.set((x, y), '|')
        elif c == '|' and neigh.count('#') >= 3: new_G.set((x, y), '#')
        elif c == '#': new_G.set((x, y), '#' if neigh.count('|') >= 1 and neigh.count('#') >= 1 else '.')
    G = new_G
    yield i, new_G
    i += 1

def one(INPUT):
  G = parse_input(INPUT)
  ITERS = 10
  ag = all_grids(G)
  for i in range(ITERS):
    _, G = next(ag)
  return len(G.detect('|')) * len(G.detect('#'))

def two(INPUT):
  G = parse_input(INPUT)
  ag = all_grids(G)
  offset, period = library.find_period(ag)
  G = library.find_periodic_state_at(ag, offset, period, 1000000000-1)
  return len(G.detect('|')) * len(G.detect('#'))

if __name__ == '__main__':
  p = puzzle.Puzzle("2018", "18")
  print(p.run(one, 0))
  print(p.run(two, 0))