#!/usr/bin/env python3
import puzzle
from collections import defaultdict

class Grid:
  def __init__(self, x=0, y=0, raw_grid=None):
    if raw_grid:
      self.x = len(raw_grid[0]) + padding * 2; self.y = len(raw_grid) + padding * 2
      self.grid = [['.' for i in range(self.x)] for j in range(self.y)]
      for j in range(len(raw_grid)):
        for i in range(len(raw_grid[0])):
          self.set((i+padding, j+padding), raw_grid[j][i])
    else:
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
  locs = dict()
  for y, row in enumerate(INPUT):
    for x, cell in enumerate(row):
      if cell == '#':
        locs[(x, y)] = '#'
  return locs

def pp(pt1, pt2):
  return (pt1[0] + pt2[0], pt1[1] + pt2[1])

def propose_move(locs, e_loc, offset):
  nw, n, ne = ((-1, -1), (0, -1), (1, -1))
  w, e = ((-1, 0), (1, 0))
  sw, s, se = ((-1, 1), (0, 1), (1, 1))
  proposals = (((nw, n, ne), (0, -1)),
               ((sw, s, se), (0, 1)),  
               ((w, nw, sw), (-1, 0)),  
               ((e, ne, se), (1, 0)),  
               )
  proposals = proposals[offset:] + proposals[:offset]
  neighbors = [pp(e_loc, dir) in locs for dir in [nw, n, ne, w, e, sw, s, se]]
  # print(neighbors)
  if neighbors.count(True) == 0:
    # print('as is', e_loc)
    return e_loc
  for clear_neighbors, prop_dir in proposals:
    neighbors = [pp(e_loc, dir) in locs for dir in clear_neighbors]
    if neighbors.count(True) == 0:
      # print('ppm')
      return pp(e_loc, prop_dir)
  # print('ERROR?')
  return e_loc


def one(INPUT):
  locs = parse(INPUT)
  # print(locs)
  dir_offset = 0
  for i in range(11):
    OFFSET = 30
    all_x = [loc[0] for loc in locs]
    all_y = [loc[1] for loc in locs]
    grid = Grid(x=max(all_x)+OFFSET, y=max(all_y)+OFFSET)
    grid.overlays = {(loc[0]+OFFSET//2, loc[1]+OFFSET//2): '#' for loc in locs}
    proposed_new_locs = defaultdict(list)
    for loc in locs:
      new_loc = propose_move(locs, loc, dir_offset)
      proposed_new_locs[new_loc].append(loc)
    new_locs = dict()
    for new_loc in proposed_new_locs:
      source_list = proposed_new_locs[new_loc]
      if len(source_list) > 1:
        for orig_loc in source_list: new_locs[orig_loc] = '#'
      else: new_locs[new_loc] = '#'
    locs = new_locs
    dir_offset = (dir_offset + 1) % 4
  
  return (max(all_x) - min(all_x)+1) * (max(all_y) - min(all_y) + 1) - len(locs)

def two(INPUT):
  locs = parse(INPUT)
  dir_offset = 0
  prev_locs = None
  for i in range(1000):
    if locs == prev_locs:
      # print('STASIS DETECTED', i)
      return i
    prev_locs = locs
    OFFSET = 30
    all_x = [loc[0] for loc in locs]
    all_y = [loc[1] for loc in locs]
    grid = Grid(x=max(all_x)+OFFSET, y=max(all_y)+OFFSET)
    grid.overlays = {(loc[0]+OFFSET//2, loc[1]+OFFSET//2): '#' for loc in locs}
    # print('after round', i)
    # print(grid)
    # print('')
    # print(max(all_x), min(all_x))
    # print(max(all_y), min(all_y))
    # print((max(all_x) - min(all_x)+1) * (max(all_y) - min(all_y) + 1) - len(locs))
    proposed_new_locs = defaultdict(list)
    for loc in locs:
      new_loc = propose_move(locs, loc, dir_offset)
      proposed_new_locs[new_loc].append(loc)
    new_locs = dict()
    for new_loc in proposed_new_locs:
      source_list = proposed_new_locs[new_loc]
      if len(source_list) > 1:
        for orig_loc in source_list: new_locs[orig_loc] = '#'
      else: new_locs[new_loc] = '#'
    locs = new_locs
    dir_offset = (dir_offset + 1) % 4

  return 0


if __name__ == '__main__':
  p = puzzle.Puzzle("2022", "23")

  p.run(one, 0) 
  p.run(two, 0) 
