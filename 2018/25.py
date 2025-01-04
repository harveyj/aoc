#!/usr/bin/env python3
import puzzle, library
import networkx as nx
import itertools

def manhattan(a, b, dims=2):
  return sum([abs(a[i] - b[i]) for i in range(dims)])

def one(INPUT):
  points = [tuple(library.ints(l)) for l in INPUT]
  G = nx.Graph()
  for a, b in itertools.combinations(points, r=2):
    G.add_node(a)
    G.add_node(b)
    if manhattan(a, b, dims=4) <= 3:
      G.add_edge(a, b)

  return len(list(nx.connected_components(G)))

def two(INPUT):
  return 20181225

if __name__ == '__main__':
  p = puzzle.Puzzle("2018", "25")
  print(p.run(one, 0))
  print(p.run(two, 0))