#!/usr/bin/env python3
import puzzle, library
import networkx as nx
import library
from functools import partial
import itertools

def one(INPUT, two=False):
  G = library.Grid(raw='\n'.join(INPUT))
  def neighbors(G, pt):
    return [loc for loc, val in G.neighbors_kv(pt, default='#') if val == '.']
  nodes = dict()
  for x in range(G.max_x()):
    for y in range(G.max_y()):
      if G.get((x, y)).isdigit():
        nodes[int(G.get((x, y)))] = (x, y)
        G.set((x, y),  '.')
  
  weights = {}
  for n1 in nodes.keys():
    for n2 in nodes.keys():
      if n1 == n2: continue
      loc1 = nodes[n1]; loc2 = nodes[n2]
      weights[(n1, n2)] = len(library.a_star_lazy(loc1, loc2, partial(library.manhattan, loc2), partial(neighbors, G))) - 1
  min_path = None; min_cost = 1000000000
  for path in itertools.permutations(range(1, 8)):
    path = [0] + list(path)
    path_cost = sum([weights[(n1, n2)] for n1, n2 in zip(path, path[1:])])
    if two: path_cost = path_cost + weights[(path[-1], 0)]
    if path_cost < min_cost:
      min_cost = path_cost
  return min_cost

def two(INPUT):
  return one(INPUT, two=True)

if __name__ == '__main__':
  p = puzzle.Puzzle("2016", "24")

  p.run(one, 0)
  p.run(two, 0)
