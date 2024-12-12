#!/usr/bin/env python3

import puzzle, library
import networkx as nx

def parse_input(INPUT):
  G = library.Grid(raw='\n'.join(INPUT))
  for x in range(G.max_x()):
    for y in range(G.max_y()):
      G.set((x, y), int(G.get((x, y))))
  return G

def one(INPUT):
  G = parse_input(INPUT)
  return 0

def two(INPUT):
  return 0

if __name__ == '__main__':
  p = puzzle.Puzzle("2021", "9")

  print(p.run(one, 0))
  print(p.run(two, 1))
