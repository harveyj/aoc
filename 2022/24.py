#!/usr/bin/env python3
import puzzle
from collections import defaultdict
import networkx as nx

class Grid:
  def __init__(self, x, y):
    self.x = x; self.y = y
    self.grid = [['.' for i in range(self.x)] for j in range(self.y)]

    self.overlays = {}

  def set(self, pt, val):
    x, y = pt
    self.grid[y][x] = val

  def get(self, pt):
    x, y = pt
    if not (0 <= x < self.x and 0<= y < self.y):
      return '.'
    return self.grid[y][x]

  def __str__(self):
    rows = []
    for y, row in enumerate(self.grid):
      row_out = []
      for x, cell in enumerate(row):
        if (x, y) in self.overlays:
          row_out.append(str(self.overlays[(x, y)]))
        else:
          row_out.append(str(cell))
      rows.append(''.join(row_out))
    return '\n'.join(rows)

def parse(INPUT):
  raw_grid = INPUT
  x = len(raw_grid[0]); y = len(raw_grid)
  g = Grid(x=x, y=y)
  print(x, y)
  print(raw_grid)
  blizzards = defaultdict(list)
  for y, row in enumerate(raw_grid):
    for x, cell in enumerate(row):
      if cell in dir_map:
        blizzards[(x, y)].append(dir_map[cell])
  return g, blizzards

dir_map = {'>': (1, 0), '<': (-1, 0), '^': (0, -1), 'v': (0, 1)}
dir_map_inv = {v: k for k, v in dir_map.items()}

def advance(grid, blizzards):
  new_blizzards = defaultdict(list)
  for pos, dirs in blizzards.items():
    for dir in dirs:
      new_pos = pos[0] + dir[0], pos[1] + dir[1]
      if new_pos[0] == 0: new_pos = grid.x - 2, new_pos[1]
      if new_pos[0] == grid.x-1: new_pos = 1, new_pos[1]
      if new_pos[1] == 0: new_pos = new_pos[0], grid.y - 2
      if new_pos[1] == grid.y-1: new_pos = new_pos[0], 1
      new_blizzards[new_pos].append(dir)
  return new_blizzards

def one(INPUT):
  grid, blizzards = parse(INPUT)

  graph = nx.DiGraph()
  for t in range(1500):
    new_blizzards = advance(grid, blizzards)
    START = (1, 0)
    END = (grid.x-2, grid.y-1)

    graph.add_edge(((1,1), t-1), (START, t))
    if not (1, 1) in new_blizzards:
      graph.add_edge((START, t-1), ((1,1), t))
    graph.add_edge((START, t), (START, 'sink'))
    # graph.add_edge((START, 'source'), (START, t))
    graph.add_edge((START, t-1), (START, t))

    graph.add_edge(((grid.x-2, grid.y-2), t-1), (END, t))
    if not (grid.x-2, grid.y-2) in blizzards:
      graph.add_edge((END, t-1), ((grid.x-2, grid.y-2), t))
    graph.add_edge((END, t-1), ((END), t))
    graph.add_edge((END, t), (END, 'sink'))

    for x in range(1, grid.x-1):
      for y in range(1, grid.y-1):
        if not (x, y) in blizzards:
          dirs = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
          for dir in dirs:
            new_pos = x + dir[0], y + dir[1]
            if 1 <= new_pos[0] < grid.x-1 and 1 <= new_pos[1] < grid.y-1 and not new_pos in new_blizzards:
              # print(((x, y), t-1), (new_pos, t))
              graph.add_edge(((x, y), t - 1), (new_pos, t))
    blizzards = new_blizzards
  # print(graph.nodes())
  leg_1 = nx.astar_path_length(graph, (START, -1), (END, 'sink'), heuristic=dist) - 1
  leg_2 = nx.astar_path_length(graph, (END, leg_1), (START, 'sink'), heuristic=dist)
  leg_3 = nx.astar_path_length(graph, (START, leg_1+leg_2), (END, 'sink'), heuristic=dist)

  print(leg_1, leg_2, leg_3)
  
  return 0

def dist(a, b):
  a = a[0]; b = b[0]
  return abs(a[0] - b[0]) + abs(a[1] - b[1])

def two(INPUT):
  return 0

if __name__ == '__main__':
  p = puzzle.Puzzle("2022", "24")

  p.run(one, 0) 
  p.run(two, 0) 
