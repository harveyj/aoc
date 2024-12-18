#!/usr/bin/env python3
import puzzle, re, library
from collections import defaultdict
import networkx as nx

def parse_input(INPUT):
  for l in INPUT: yield library.ints(l)

def puzz(INPUT, xmax, ymax, input_slice):
  G = library.Grid(x=xmax, y=ymax)
  poison = parse_input(INPUT[:input_slice])
  for p in poison:
    G.set(p, '#')
  graph = nx.Graph()
  for x in range(G.max_x()):
    for y in range(G.max_y()):
      if G.get((x, y)) == '.':
        for neigh, neigh_val in G.neighbors_kv((x, y)):
          if neigh_val == '.':
            graph.add_edge((x, y), neigh)
  try:
      path = nx.shortest_path(graph, (0,0), (xmax-1, ymax-1))
      return len(path) - 1 # -1 is fencepost
  except nx.NetworkXNoPath:
    return -1
    
def one(INPUT):
  return puzz(INPUT, 71, 71, 1024)

def two(INPUT):
  lo = 0; hi = len(INPUT)
  while True:
    i = (lo + hi)//2
    if puzz(INPUT, 71, 71, i) != -1 and puzz(INPUT, 71, 71, i+1) == -1:
      return INPUT[i].replace(',', '-') # ugly hack bc my answer file is csv
    if puzz(INPUT, 71, 71, i+1) == -1:
      hi = i
    else: lo = i


if __name__ == '__main__':
  p = puzzle.Puzzle("2024", "18")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')
