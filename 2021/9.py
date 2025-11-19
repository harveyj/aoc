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
      if len([n for n in neigh if n > G.get((x,y), default=9)]) == len(neigh):
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
      val = G.get((x, y))
      if val == 9: continue
      for neigh, neigh_val in G.neighbors_kv((x, y)):
        if neigh_val in [None, 9]: continue
        if val > neigh_val:
          DG.add_edge(neigh, (x, y))
  basins = [nx.descendants(DG, lp) | {lp} for lp in low_pts] 
  all = list(chain.from_iterable(basins))
  b_sizes = sorted([len(basin) for basin in basins])
  return b_sizes[-3] * b_sizes[-2] * b_sizes[-1]

if __name__ == '__main__':
  p = puzzle.Puzzle("2021", "9")

  print(p.run(one, 0))
  print(p.run(two, 0))
