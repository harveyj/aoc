#!/usr/bin/env python3
import puzzle, library, math
import networkx as nx

def one(INPUT, two=False):
  invals = [tuple(library.ints(l)) for l in INPUT]
  dist = {}
  G = nx.Graph()
  for i, pt1 in enumerate(invals):
    G.add_node(pt1)
    for j, pt2 in enumerate(invals[i+1:]):
      dist[(pt1, pt2)] = (pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1] )**2 + (pt1[2] - pt2[2])**2
  rev_dist = [(val, key) for key, val in dist.items()]
  rev_dist.sort()
  paths_added = 0
  for _, pts in rev_dist:
    a, b = pts
    if not nx.has_path(G, a, b): 
      G.add_edge(a, b)
    paths_added += 1
    if two:
      if len(list(nx.connected_components(G))) == 1:
        return a[0] * b[0]
    else:
      if paths_added == 1000: break
  cc = sorted([len(cli) for cli in nx.connected_components(G)])
  return cc[-3] * cc[-2] * cc[-1] 

def two(INPUT):
  return one(INPUT, two=True)

if __name__ == '__main__':
  p = puzzle.Puzzle("2025", "8")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')
