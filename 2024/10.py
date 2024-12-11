#!/usr/bin/env python3
import puzzle, library
import networkx as nx

MAX = 11

def parse_input(INPUT):
  G = library.Grid(raw='\n'.join(INPUT))
  DG = nx.DiGraph()
  for x in range(G.max_x()):
    for y in range(G.max_y()):
      c = G.get((x, y), default=MAX)
      for pt, val in G.neighbors_kv((x, y)):
        if val == None: continue
        if int(c) - int(val) == 1:
          DG.add_edge(pt, (x, y))
  return G, DG

def one(INPUT, two=False):
  G, DG = parse_input(INPUT)
  # print(DG)
  total = 0
  starts = G.detect('0')
  ends = G.detect('9')
  for st in starts:
    for end in ends:
      num_paths = len(list(nx.all_simple_paths(DG, st, end)))
      if num_paths > 0:
        total += num_paths if two else 1
  return total

def two(INPUT):
  return one(INPUT, two=True)

if __name__ == '__main__':
  p = puzzle.Puzzle("2024", "10")
  print(p.run(one, 0))
  print(p.run(two, 0))