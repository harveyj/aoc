#!/usr/bin/env python3
import puzzle
import re
import networkx as nx

def parse(INPUT):
  def get_cell(grid, x, y):
    if x < 0 or x >= len(grid[0]):
      return '}' # Greater than any legal character by >2
    if y < 0 or y >= len(grid):
      return '}' # Greater than any legal character by >2
    return grid[y][x]

  G = nx.DiGraph()
  raw_grid = [list(l) for l in INPUT.split('\n')]
  start = None; end = None; all_a = []
  for y, row in enumerate(raw_grid):
    for x, c in enumerate(row):
      if c == 'S':
        row[x] = 'a'
        start = (x, y)
      elif c == 'E':
        row[x] = 'z'
        end = (x, y)
      elif c == 'a':
        all_a.append((x, y))

      G.add_node((x, y))
  for y, row in enumerate(raw_grid):
    for x, c in enumerate(row):
      delts = [(0, 1), (0, -1), (1, 0), (-1, 0)]
      for dx, dy in delts:
        n_x = x + dx; n_y = y + dy
        asc = ord(c)
        asc_adj = ord(get_cell(raw_grid, n_x, n_y))
        if asc+2 > asc_adj:
          G.add_edge((x, y), (n_x, n_y)) 
  return G, start, end, all_a

def one(INPUT):
  G, start, end, _ = parse(INPUT)
  sp = nx.shortest_path(G, start, end)
  print(sp)
  return len(sp) - 1

def two(INPUT):
  G, start, end, all_a = parse(INPUT)
  sp = []; min_len_sp = 1000000
  for st in all_a:
    try:
      new_sp = nx.shortest_path(G, st, end)
    except: pass
    if len(new_sp) < min_len_sp:
      sp = new_sp
      min_len_sp = len(sp)
  return len(sp) - 1

p = puzzle.Puzzle("12")
p.run(one, 1)
p.run(two, 0)
