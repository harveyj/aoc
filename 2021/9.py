#!/usr/bin/env python3

import puzzle, library
import networkx as nx
from itertools import chain

def parse_input(INPUT):
  G = library.Grid(raw='\n'.join(INPUT))
  for x in range(G.max_x()):
    for y in range(G.max_y()):
      G.set((x, y), int(G.get((x, y))))
  return G

def detect_low(G):
  low_vals = []
  low_pts = set()
  for x in range(G.max_x()):
    for y in range(G.max_y()):
      neigh = list(G.neighbors((x, y)))
      if len([n for n in neigh if n > G.get((x,y))]) == len(neigh):
        low_vals.append(1+G.get((x, y)))
        low_pts.add((x, y))
  return low_vals, low_pts

def one(INPUT):
  G = parse_input(INPUT)
  low_vals, low_pts = detect_low(G)
  return sum(low_vals)

def two(INPUT):
  G = parse_input(INPUT)
  low_vals, low_pts = detect_low(G)
  DG = nx.DiGraph()
  for x in range(G.max_x()):
    for y in range(G.max_y()):
      DG.add_node((x, y))
      for neigh, val in G.neighbors_kv((x, y)):
        if val in [None, 9]: continue
        if val - 1 == G.get((x, y)):
          DG.add_edge((x, y), neigh)
  basins = [nx.descendants(DG, lp) for lp in low_pts]
  all = list(chain.from_iterable(basins))
  # for x in range(G.max_x()):
  #   for y in range(G.max_y()):
  #     if (x, y) not in all:
  #       print((x,y), G.get((x, y)))
  # print(DG.edges((99,1)))
  # print((99, 64) in low_pts)
  # +1 is to account for the bottom
  b_sizes = sorted([len(basin) + 1 for basin in basins])
  # oh no test works real vals don't
  return b_sizes[-3] * b_sizes[-2] * b_sizes[-1]

if __name__ == '__main__':
  p = puzzle.Puzzle("2021", "9")

  print(p.run(one, 0))
  print(p.run(two, 0))
