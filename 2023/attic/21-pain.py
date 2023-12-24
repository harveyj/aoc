#!/usr/bin/env python3
import puzzle, re, functools, networkx as nx
from collections import defaultdict
import numpy

def parse_input(INPUT):
  return puzzle.Grid(raw=INPUT)

dirs = ((0, 1), (0, -1), (1, 0), (-1, 0))

@functools.cache
def possibles(G, loc, remaining):
  total = set()
  if remaining == 0:
    return set([loc])
  for dx, dy in dirs:
    new_pt = puzzle.pt_add(loc, (dx, dy))
    if G.get(new_pt) != '#':
      total = total.union(possibles(G, new_pt, remaining - 1))
  return total

def one(INPUT):
  G = parse_input(INPUT)

  for x in range(G.max_x()):
    for y in range(G.max_y()):
      if G.get((x, y)) == 'S':
        S = (x, y)
  pts = possibles(G, S, 40)
  for p in pts:
    # print(p)
    G.overlays[p] = 'O'
  print(G)
  return len(pts)

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


def two(INPUT):
  grid = parse_input(INPUT)
  G = nx.Graph()

  for x in range(grid.max_x()):
    for y in range(grid.max_y()):
      pt = (x,y)
      if grid.get(pt) == 'S':
        S = pt
        grid.set(pt, '.')

  scale_factor = 30
  scaled = puzzle.Grid(x=grid.max_x()*scale_factor, y=grid.max_y()*scale_factor)
  for x in range(scaled.max_x()):
    for y in range(scaled.max_y()):
      scaled.set((x, y), grid.get((x % grid.max_x(), y % grid.max_y())))
  S = ((S[0] + grid.max_x()*scale_factor//2,
        S[1] + grid.max_y()*scale_factor//2))
  s_idx = S[0] // grid.max_x(), S[1] // grid.max_y()
  print(s_idx)

  for x in range(scaled.max_x()):
    for y in range(scaled.max_y()):
      pt = (x,y)
      if scaled.get(pt, default='#') != '#':
        G.add_node(pt)
        for d in dirs:
          new_pt = puzzle.pt_add(pt, d)
          if scaled.get(new_pt, default='#') != '#':
            G.add_edge(pt, new_pt)
  subgrids = defaultdict(int)

  period = 11
  rp = reachable_plots(G, S, s_idx, 89, period, grid.max_x(), grid.max_y())
  rp2 = reachable_plots(G, S, s_idx, 100, period, grid.max_x(), grid.max_y())
  print(rp)
  print(rp2)
  # print('rp at 100 should equal 6536 ', rp)

  n_count = 501
  possible_outcome_map = {}

  shortest_paths = nx.single_source_shortest_path_length(G, source=S)
  for step_n in range(n_count):
    scaled.overlays = {}
    total = 0
    for target, length in shortest_paths.items():
      if length <= step_n and length % 2 == step_n % 2:
        scaled.overlays[target] = 'O'
        total += 1
        subgrids[((target[0] // grid.max_x(), target[1] // grid.max_y()), step_n)] += 1
    possible_outcome_map[step_n] = total

  grid_n = s_idx[0], s_idx[1] - 4
  grid_nn = s_idx[0], s_idx[1] - 5
  grid_s = s_idx[0], s_idx[1] + 4
  grid_ss = s_idx[0], s_idx[1] + 5
  grid_e = s_idx[0]+4, s_idx[1]
  grid_ee = s_idx[0]+5, s_idx[1]

  # for i in range(n_count):
  #   print('%i,%i,%i,%i,%i' % (i, subgrids[grid_e, i], subgrids[grid_s, i], subgrids[grid_ee, i], subgrids[grid_ss, i]))


  # print(possible_outcome_map)
  out = 0
  return out

p = puzzle.Puzzle("21")
# p.run(one, 0)
# p.run(one_b, 1)

p.run(two, 1)
