#!/usr/bin/env python3
import puzzle, re, library
from collections import defaultdict
import networkx as nx
import itertools
from collections import defaultdict

def parse_input(INPUT):
  return library.Grid(raw='\n'.join(INPUT))

DIRS = '>v<^'
DIRS_TO_COORDS = {a:b for a, b in zip(DIRS, library.DIRS_CARDINAL)}
DIR_DELT = [-1, 0, 1]
TURNS = {('/', '^'): '>',
         ('/', '<'): 'v',
         ('/', '>'): '^',
         ('/', 'v'): '<',
         ('\\', '^'): '<',
         ('\\', 'v'): '>',
         ('\\', '>'): 'v',
         ('\\', '<'): '^',
         }

def one(INPUT, two=False):
  G = parse_input(INPUT)
  # dir, next turn, loc

  carts = list(itertools.chain(*[[(dir, 0, loc) for loc in G.detect(dir)] for dir in DIRS]))
  for (dir, next_turn, loc) in carts:
    G.set(loc, '-' if dir in '<>' else '|')

  for i in range(100000):
    carts = sorted(carts, key=lambda a: (a[2][1], a[2][0]))
    new_locs = set()
    old_locs = set([a[2] for a in carts])
    remove_locs = set()
    for i, cart in enumerate(carts):
      (dir, next_turn, loc) = cart
      # print(loc, end = ',')
      loc = library.pt_add(loc, DIRS_TO_COORDS[dir])
      if loc in new_locs or loc in old_locs:
        if two:
          remove_locs.add(loc)
        else: return '.'.join(map(str, loc))
      new_locs.add(loc)
      if (G.get(loc), dir) in TURNS:
        dir = TURNS[G.get(loc), dir]
      elif G.get(loc) == '+':
        dir_idx = (DIRS.index(dir) + DIR_DELT[next_turn] + 4) % len(DIRS)
        dir = DIRS[dir_idx]

        next_turn = (next_turn + 1) % len(DIR_DELT)
      carts[i] = (dir, next_turn, loc)
    carts = [c for c in carts if c[2] not in remove_locs]
    G.overlays = {loc: dir for (dir, next_turn, loc) in carts}
    if len(carts) == 1:
      return '.'.join(map(str, carts[0][2]))

    # Fun to watch it step!
    # print('')
    # print(G)
    # input()

def two(INPUT):
  return one(INPUT, two=True)

if __name__ == '__main__':
  p = puzzle.Puzzle("2018", "13")
  print(p.run(one, 0))
  print(p.run(two, 0))
