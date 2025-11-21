#!/usr/bin/env python3
import puzzle, networkx as nx
from collections import defaultdict
import library

def parse_input(INPUT):
  return library.Grid(raw='\n'.join(INPUT))

dirs = ((0, 1), (0, -1), (1, 0), (-1, 0))

def num_reachable(G, S, steps, odd):
  shortest_paths = nx.single_source_shortest_path_length(G, source=S)
  total = 0
  for target, length in shortest_paths.items():
    if length <= steps and length % 2 == (1 if odd else 0):
      total += 1
  return total


def one(INPUT):
  grid = parse_input(INPUT)
  G = nx.Graph()
  for x in range(grid.max_x()):
    for y in range(grid.max_y()):
      pt = (x,y)
      if grid.get(pt) == 'S':
        S = pt
        grid.set(pt, '.')
      if grid.get(pt, default='#') != '#':
        G.add_node(pt)
        for d in dirs:
          new_pt = library.pt_add(pt, d)
          if grid.get(new_pt, default='#') != '#':
            G.add_edge(pt, new_pt)

  shortest_paths = nx.single_source_shortest_path_length(G, source=S)
  for step_n in range(65):
    grid.overlays = {}
    total = 0
    for target, length in shortest_paths.items():
      if length <= step_n and length % 2 == step_n % 2:
        grid.overlays[target] = 'O'
        total += 1
  return total

# https://github.com/villuna/aoc23/wiki/A-Geometric-solution-to-advent-of-code-2023,-day-21 is amazing
def two(INPUT):
  grid = parse_input(INPUT)
  G = nx.Graph()
  for x in range(grid.max_x()):
    for y in range(grid.max_y()):
      pt = (x,y)
      if grid.get(pt) == 'S':
        S = pt
        grid.set(pt, '.')
      if grid.get(pt, default='#') != '#':
        G.add_node(pt)
        for d in dirs:
          new_pt = library.pt_add(pt, d)
          if grid.get(new_pt, default='#') != '#':
            G.add_edge(pt, new_pt)

  num_even = num_reachable(G, S, 131, odd=False)
  num_odd = num_reachable(G, S, 131, odd=True)
  num_odd_corner = num_reachable(G, S, 131, odd=True) - num_reachable(G, S, 65, odd=True)
  num_even_corner = num_reachable(G, S, 131, odd=False) - num_reachable(G, S, 65, odd=False)
  n = (26501365 - 65) // 131
  tot = (n+1)*(n+1)*num_odd + (n)*(n)*num_even - (n+1) * num_odd_corner + (n) * num_even_corner
  return tot

if __name__ == '__main__':
  p = puzzle.Puzzle("2023", "21")

  # p.run(one, 0) 
  print(p.run(two, 0))
