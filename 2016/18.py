#!/usr/bin/env python3
import puzzle, library
import re

def parse(INPUT):
  pat = re.compile('(\w+)+')
  for l in INPUT:
    yield re.match(pat, l).groups()

LEFT, CENTER, RIGHT = (-1, -1), (0, -1), (1, -1)
TRAPS = ('^^.', '.^^', '^..', '..^')

def one(INPUT, two=False):
  seed = INPUT[0]
  G = library.Grid(x=len(seed), y=400000 if two else 40)
  for x, c in enumerate(seed):
    G.set((x, 0), c)
  for y in range(1, G.max_y()):
    for x in range(0, G.max_x()):
      l_loc = library.pt_add(LEFT, (x, y))
      c_loc = library.pt_add(CENTER, (x, y))
      r_loc = library.pt_add(RIGHT, (x, y))
      l = G.get(l_loc, default='.')
      c = G.get(c_loc, default = '.')
      r = G.get(r_loc, default = '.')
      trap = l+c+r in TRAPS
      G.set((x, y), '^' if trap else '.')
  return len(G.detect('.'))

def two(INPUT):
  return one(INPUT, two=True)

if __name__ == '__main__':
  p = puzzle.Puzzle("2016", "18")

  p.run(one, 0)
  p.run(two, 0)
