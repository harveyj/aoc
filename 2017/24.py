#!/usr/bin/env python3
import puzzle, library
import re
import networkx as nx
from collections import deque
def parse(INPUT):
  for l in INPUT:
    yield tuple(map(int, l.split('/')))


def onetwo(INPUT):
  G = nx.Graph()
  for s, e in parse(INPUT):
    if G.has_edge(s, e):
      G.add_edge(s, e, G.get_edge_data(s, e) + 1)
    else:
      G.add_edge(s, e, data=1)

  all_paths = []
  paths = deque([[0]])
  while True:
    if len(paths) == 0: break
    path = paths.pop()
    all_paths.append(path)
    for s, e in G.edges(path[-1]):
      num_permitted = G.get_edge_data(s, e)
      num_present = list(zip(path, path[1:])).count((s, e))
      num_present += list(zip(path[1:], path)).count((s, e))
      # print(f'npres: {num_present}, nperm:{num_permitted}')
      if num_present >= num_permitted['data']: continue
      paths.appendleft(path + [e])
  # print(all_paths)
  path_len_weights = [(len(path), sum([a+b for a, b in zip(path, path[1:])])) for path in all_paths]
  max_weight = max([b for _, b in path_len_weights])
  max_len = max([a for a, _ in path_len_weights])
  two = max([b for a, b in path_len_weights if a == max_len])
  return max_weight, two

def one(INPUT):
  return onetwo(INPUT)[0]
def two(INPUT):
  return onetwo(INPUT)[1]

if __name__ == '__main__':
  p = puzzle.Puzzle("2017", "24")
  p.run(one, 0)
  p.run(two, 0)
