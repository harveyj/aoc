#!/usr/bin/env python3
import puzzle, library
from collections import defaultdict
import networkx as nx

def parse_input(INPUT):
  return library.Grid(raw='\n'.join(INPUT))

def one(INPUT):
  G = parse_input(INPUT)
  S = G.detect('S')[0]
  E = G.detect('E')[0]
  graph = G.graph()
  hist = defaultdict(int)
  path = list(nx.all_simple_paths(graph, S, E))[0]
  skip = 101
  cheats = set()
  for i, node in enumerate(path):
    for j, node2 in enumerate(path[i+skip:]):
      n1x, n1y = node; n2x, n2y = node2
      if abs(n1x - n2x) == 2 and n1y == n2y and G.get(((n1x+n2x)//2, n2y)) == '#':
        cheats.add(((n1x+n2x)//2, n2y))
        hist[j-1] += 1
      if abs(n1y - n2y) == 2 and n1x == n2x and G.get((n1x, (n1y+n2y)//2)) == '#':
        cheats.add((n1x, (n1y+n2y)//2))
        hist[j-1] += 1
  return len(cheats)

def two(INPUT):
  G = parse_input(INPUT)
  S = G.detect('S')[0]
  E = G.detect('E')[0]
  graph = G.graph()
  hist = defaultdict(int)
  path = list(nx.all_simple_paths(graph, S, E))[0]
  skip = 101
  cheats = set()
  for i, node in enumerate(path):
    for j, node2 in enumerate(path[i+skip:]):
      teleport_time = library.manhattan(node, node2)
      saved = j+skip-teleport_time
      if teleport_time <= 20 and saved >= 100:
        cheats.add((node, node2))
        hist[saved] += 1
  return len(cheats)

if __name__ == '__main__':
  p = puzzle.Puzzle("2024", "20")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')
