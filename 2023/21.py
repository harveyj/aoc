#!/usr/bin/env python3
import puzzle, re, functools, networkx as nx
from collections import defaultdict
import numpy

def parse_input(INPUT):
  return puzzle.Grid(raw=INPUT)

dirs = ((0, 1), (0, -1), (1, 0), (-1, 0))

def one_b(INPUT):
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
          new_pt = puzzle.pt_add(pt, d)
          if grid.get(new_pt, default='#') != '#':
            G.add_edge(pt, new_pt)

  shortest_paths = nx.single_source_shortest_path_length(G, source=S)
  # print(shortest_paths)
  for step_n in range(65):
    grid.overlays = {}
    total = 0
    for target, length in shortest_paths.items():
      if length <= step_n and length % 2 == step_n % 2:
        grid.overlays[target] = 'O'
        total += 1
    print(step_n, total)
    # print(grid)

def find_period(s_idx, subgrids, n_count):
  grid_n = s_idx[0], s_idx[1] - 4
  grid_nn = s_idx[0], s_idx[1] - 5
  print(grid_n, grid_nn)
  # find the first i such that grid_n != 0
  # find the first j such that grid_nn != 0
  # period = j - i ?
  for i in range(n_count):
    if subgrids[(grid_n, i)] > 0:
      break
  for j in range(n_count):
    if subgrids[(grid_nn, j)] > 0:
      break
  print('PERIOD',j,i, j-i)

def reachable_plots(scaled_grid, S, s_idx, n_steps, period, max_x, max_y):
  # offset_steps is some number n such that offset_steps % period == n_steps % period
  offset_steps = n_steps % period + period * 4
  # TODO: undo this
  offset_steps = n_steps
  shortest_paths = nx.single_source_shortest_path_length(scaled_grid, source=S)
  offset_reachable = 0
  subgrids = defaultdict(int)
  # calculate the number of plots reachable from offset_steps
  for target, length in shortest_paths.items():
    if length <= offset_steps and length % 2 == offset_steps % 2:
      offset_reachable += 1
      subgrids[((target[0] // max_x, target[1] // max_y), offset_steps)] += 1
  print(offset_steps, offset_reachable)
  # print(subgrids)
  # calculate n, s, e, w
  # we can initialize to any valid grid
  first_loc = list(subgrids.keys())[0][0]
  top_grid, bottom_grid, left_grid, right_grid = first_loc, first_loc, first_loc, first_loc
  for k in subgrids:
    grid_loc = k[0]
    # print(grid_loc, left_grid)
    if grid_loc[0] < left_grid[0]: left_grid = grid_loc
    if grid_loc[1] <= top_grid[1]:
      print('replacing', top_grid, grid_loc)
      top_grid = grid_loc
    if grid_loc[0] > right_grid[0]: right_grid = grid_loc
    if grid_loc[1] > bottom_grid[1]: bottom_grid = grid_loc

  ne1_grid = top_grid[0] + 1, top_grid[1] + 1
  ne2_grid = top_grid[0] + 2, top_grid[1] + 2
  nw1_grid = top_grid[0] - 1 , top_grid[1] + 1
  nw2_grid = top_grid[0] - 2 , top_grid[1] + 2

  se1_grid = bottom_grid[0] + 1, bottom_grid[1] - 1
  se2_grid = bottom_grid[0] + 2, bottom_grid[1] - 2
  sw1_grid = bottom_grid[0] - 1 , bottom_grid[1] - 1
  sw2_grid = bottom_grid[0] - 2 , bottom_grid[1] - 2

  # calculate filled
  filled = s_idx

  grid_indices = [top_grid, bottom_grid, left_grid, right_grid, ne1_grid, ne2_grid, se1_grid, se2_grid, filled]
  return grid_indices, [subgrids[(g, n_steps)] for g in grid_indices]


p = puzzle.Puzzle("21")
p.run(one_b, 1)
