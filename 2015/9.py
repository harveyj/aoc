#!/usr/bin/env python3
import puzzle
import re
import networkx
from itertools import permutations

def parse(INPUT):
  pat = re.compile('(\w+) to (\w+) = (\d+)')
  for l in INPUT.split('\n'):
    yield re.match(pat, l).groups()

def one(INPUT):
  G = networkx.Graph()
  for a, b, dist in parse(INPUT):
    G.add_edge(a, b, weight=int(dist))
  shortest_cost = None
  shortest_path = None
  for path in permutations(G.nodes()):
    path_cost = sum(G[u][v]['weight'] for u, v in zip(path[:-1], path[1:]))
    if shortest_cost is None or path_cost < shortest_cost:
      shortest_cost = path_cost
      shortest_path = path
  return shortest_cost, shortest_path

def two(INPUT):
  G = networkx.Graph()
  for a, b, dist in parse(INPUT):
    G.add_edge(a, b, weight=int(dist))
  longest_cost = None
  longest_path = None
  for path in permutations(G.nodes()):
    path_cost = sum(G[u][v]['weight'] for u, v in zip(path[:-1], path[1:]))
    if longest_cost is None or path_cost > longest_cost:
      longest_cost = path_cost
      longest_path = path
  return longest_cost, longest_path

p = puzzle.Puzzle("9")
p.run(one, 0)
p.run(two, 0)
