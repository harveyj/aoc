#!/usr/bin/env python3
from curses import raw
import puzzle
import re

class Grid:
  def __init__(self, raw_grid):
    self.x = len(raw_grid[0]); self.y = len(raw_grid)
    self.grid = [[raw_grid[j][i] for i in range(self.x)] for j in range(self.y)]
    self.overlays = {}

  def set(self, pt, val):
    x, y = pt
    self.grid[y][x] = val

  def get(self, pt):
    x, y = pt
    return self.grid[y][x]

  def __str__(self):
    rows = []
    for y, row in enumerate(self.grid):
      row_out = []
      for x, cell in enumerate(row):
        if (x, y) in self.overlays:
          row_out.append(self.overlays[(x, y)])
        else:
          row_out.append(cell)
      rows.append(''.join(row_out))
    return '\n'.join(rows)

def get_next_loc(loc, bearing, grid):
  x, y = loc; dx, dy = bearing
  x, y = (x + dx) % grid.x, (y + dy) % grid.y
  while grid.get((x, y)) == ' ':
    x, y = (x + dx) % grid.x, (y + dy) % grid.y
  return x, y

def parse(INPUT):
  def parse_instr(instr):
    if instr in ['L', 'R']:
      return instr
    else:
      return int(instr)
  raw_grid, raw_instrs = INPUT.split('\n\n')
  instrs = [parse_instr(instr) for instr in re.split('(\d+)', raw_instrs) if instr]
  raw_grid = raw_grid.split('\n')
  max_len = max([len(row) for row in raw_grid])
  raw_grid = [[row[x] if x < len(row) else ' ' for x in range(max_len)] for row in raw_grid]
  return raw_grid, instrs

def one(INPUT):
  bearings = [(1, 0), (0, 1), (-1, 0), (0, -1)]
  bearings_signature = ['>', 'v', '<', '^']
  dir_idx = 0
  raw_grid, instrs = parse('\n'.join(INPUT))
  loc = (raw_grid[0].index('.'), 0)
  grid = Grid(raw_grid)
  for instr in instrs:
    bearing = bearings[dir_idx]
    if instr == 'R':
      dir_idx = (dir_idx + 1) % 4 
    elif instr == 'L':
      dir_idx = (dir_idx - 1) % 4
    else:
      for i in range(instr):
        next_loc = get_next_loc(loc, bearing, grid)
        if grid.get(next_loc) == '#':
          break
        loc = next_loc
        if loc not in grid.overlays:
          grid.overlays[loc] = bearings_signature[dir_idx]
  return 1000 * (loc[1]+1) + 4 * (loc[0] +1) + dir_idx

def get_next_loc_and_bearing(loc, bearing, lb_map):
  if (loc, bearing) in lb_map:
    # print('teleport', lb_map[(loc, bearing)])
    return lb_map[(loc, bearing)]
  x, y = loc; dx, dy = bearing
  x, y = (x + dx), (y + dy)
  return (x, y), bearing

# def find_edges(grid):
#   first_x = [i for i in range(grid.y+1)]
#   first_y = [i for i in range(grid.x+1)]
#   last_x = [i for i in range(grid.y+1)]
#   last_y = [i for i in range(grid.x+1)]
#   for y in range(grid.y):
#     x = 0
#     while x < grid.x and grid.get((x, y)) == ' ':
#       x += 1
#       first_x[y] = x
#     while x < grid.x:
#       while x < grid.x and grid.get((x, y)) != ' ':
#         x += 1
#         last_x[y] = x
#       x += 1
#   for x in range(grid.x):
#     y = 0
#     while y < grid.y and grid.get((x, y)) == ' ':
#       y += 1
#       first_y[x] = y
#     while y < grid.y:
#       while y < grid.y and  grid.get((x, y)) != ' ':
#         y += 1
#         last_y[x] = y
#       y += 1

#   return first_x, last_x, first_y, last_y

# def one(INPUT):
#   one_lb_map = dict()
#   first_x, last_x, first_y, last_y = find_edges(grid)
#   for x in range(grid.x):
#     one_lb_map[(x, first_y[x]), (0, -1)] = (x, last_y[x]), (0, -1)
#     one_lb_map[(x, last_y[x]), (0, 1)] = (x, first_y[x]), (0, 1)
#   for y in range(grid.y):
#     one_lb_map[(first_x[y], y), (-1, 0)] = (last_x[y], y), (-1, 0)
#     one_lb_map[(last_x[y], y), (1, 0)] = (first_x[y], y), (1, 0)
#   return two(INPUT, one=True)

def pair_edge(lb_map, a_1, a_2, b_1, b_2, bearing_1, bearing_2):
  x_1, y_1 = a_1; x_2, y_2 = a_2; x_3, y_3 = b_1;  x_4, y_4 = b_2; 
  dax = (x_2 - x_1) // abs(x_2 - x_1) if x_2 != x_1 else 0
  day = (y_2 - y_1) // abs(y_2 - y_1) if y_2 != y_1 else 0
  dbx = (x_4 - x_3) // abs(x_4 - x_3) if x_4 != x_3 else 0
  dby = (y_4 - y_3) // abs(y_4 - y_3) if y_4 != y_3 else 0
  ax, ay = a_1
  bx, by = b_1
  if dax and day or dbx and dby:
    print('ERROR', a_1, a_2)
  if abs(x_2 - x_1) not in [0,49] or abs(y_2 - y_1) not in [0,49] :
    print('ERROR', a_1, a_2)
  for i in range(max(abs(x_2 - x_1), abs(y_2 - y_1)) + 1):
    # print('pairing', (ax, ay), (bx, by))
    lb_map[(ax, ay), bearing_1] = ((bx, by), bearing_2)
    ax += dax; ay += day; bx += dbx; by += dby

def edges_one(grid):
  lb_map = dict()
  a_11, a_12, a_21, a_22 = (8, 0), (11, 0), (8, 3), (11, 3) 
  b_11, b_12, b_21, b_22 = (0, 4), (3, 4), (0, 7), (3, 7) 
  c_11, c_12, c_21, c_22 = (4, 4), (7, 4), (4, 7), (7, 7) 
  d_11, d_12, d_21, d_22 = (8, 4), (11, 4), (8, 7), (11, 7) 
  e_11, e_12, e_21, e_22 = (8, 8), (11, 8), (8, 11), (11, 11) 
  f_11, f_12, f_21, f_22 = (12, 8), (15, 8), (12, 11), (15, 11) 

  # for pt in (a_11, a_12, a_21, a_22): grid.overlays[pt] = 'a'
  # for pt in (b_11, b_12, b_21, b_22): grid.overlays[pt] = 'b'
  # for pt in (c_11, c_12, c_21, c_22): grid.overlays[pt] = 'c'
  # for pt in (d_11, d_12, d_21, d_22): grid.overlays[pt] = 'd'
  # for pt in (e_11, e_12, e_21, e_22): grid.overlays[pt] = 'e'
  # for pt in (f_11, f_12, f_21, f_22): grid.overlays[pt] = 'f'

  # a top with b top
  pair_edge(lb_map, a_11, a_12, b_12, b_11, (0, -1), (0, 1))
  # a left with c top
  pair_edge(lb_map, a_11, a_21, c_12, c_11, (-1, 0), (0, 1))
  # a down as is
  # a right with f right
  pair_edge(lb_map, a_12, a_22, f_22, f_12, (1, 0), (-1, 0))

  # b left with f down
  pair_edge(lb_map, b_11, b_21, f_21, f_22, (-1, 0), (0, -1))
  # b top with a top
  pair_edge(lb_map, b_11, b_12, a_12, a_11, (0, -1), (0, 1))
  # b right as is
  # b down with e down
  pair_edge(lb_map, b_12, b_22, e_22, e_12, (0, 1), (0, -1))

  # c left as is
  # c top with a right
  pair_edge(lb_map, c_11, c_12, a_11, a_21, (0, -1), (1, 0))
  # c right as is
  # c down with e left
  pair_edge(lb_map, c_21, c_22, e_11, e_21, (0, 1), (1, 0))

  # d right with f top
  pair_edge(lb_map, d_12, d_22, f_12, f_11, (1, 0), (0, 1))

  # e left with c bottom
  pair_edge(lb_map, e_11, e_12, c_21, c_11, (-1, 0), (0, -1))
  # e bottom with b bottom
  pair_edge(lb_map, e_21, e_22, b_22, b_21, (0, 1), (0, -1))

  # f up with d right
  pair_edge(lb_map, f_11, f_12, d_22, d_12, (0, -1), (-1, 0))
  # f right with a right
  pair_edge(lb_map, f_22, f_12, a_12, a_22, (1, 0), (-1, 0))
  # f down with b left
  pair_edge(lb_map, f_21, f_22, b_11, b_21, (0, 1), (1, 0))
  return lb_map

def edges_two(grid):
  lb_map = dict()
  width = 50
  start_x = 50; start_y = 0
  a_11, a_12, a_21, a_22 = (start_x, start_y), (start_x+width-1, start_y), (start_x, start_y+width-1), (start_x+width-1, start_y+width-1) 
  start_x = 100; start_y = 0
  b_11, b_12, b_21, b_22 = (start_x, start_y), (start_x+width-1, start_y), (start_x, start_y+width-1), (start_x+width-1, start_y+width-1) 
  start_x = 50; start_y = 50
  c_11, c_12, c_21, c_22 = (start_x, start_y), (start_x+width-1, start_y), (start_x, start_y+width-1), (start_x+width-1, start_y+width-1) 
  start_x = 0; start_y = 100
  d_11, d_12, d_21, d_22 = (start_x, start_y), (start_x+width-1, start_y), (start_x, start_y+width-1), (start_x+width-1, start_y+width-1) 
  start_x = 50; start_y = 100
  e_11, e_12, e_21, e_22 = (start_x, start_y), (start_x+width-1, start_y), (start_x, start_y+width-1), (start_x+width-1, start_y+width-1) 
  start_x = 0; start_y = 150
  f_11, f_12, f_21, f_22 = (start_x, start_y), (start_x+width-1, start_y), (start_x, start_y+width-1), (start_x+width-1, start_y+width-1) 

  for pt in (a_11, a_12, a_21, a_22): grid.overlays[pt] = 'a'
  for pt in (b_11, b_12, b_21, b_22): grid.overlays[pt] = 'b'
  for pt in (c_11, c_12, c_21, c_22): grid.overlays[pt] = 'c'
  for pt in (d_11, d_12, d_21, d_22): grid.overlays[pt] = 'd'
  for pt in (e_11, e_12, e_21, e_22): grid.overlays[pt] = 'e'
  for pt in (f_11, f_12, f_21, f_22): grid.overlays[pt] = 'f'

  # a top with f left
  pair_edge(lb_map, a_11, a_12, f_11, f_21, (0, -1), (1, 0))
  # a left with d left
  pair_edge(lb_map, a_11, a_21, d_21, d_11, (-1, 0), (1, 0))
  # a right as is
  # a down as is

  # b top with f down
  pair_edge(lb_map, b_11, b_12, f_21, f_22, (0, -1), (0, -1))
  # b left as is
  # b right with e right
  pair_edge(lb_map, b_12, b_22, e_22, e_12, (1, 0), (-1, 0))
  # b down with c right
  pair_edge(lb_map, b_21, b_22, c_12, c_22, (0, 1), (-1, 0))

  # c up as is
  # c right with b down
  pair_edge(lb_map, c_12, c_22, b_21, b_22, (1, 0), (0, -1))
  # c left with d top
  pair_edge(lb_map, c_11, c_21, d_11, d_12, (-1, 0), (0, 1))
  # c down as is

  # d top with c left
  pair_edge(lb_map, d_11, d_12, c_11, c_21, (0, -1), (1, 0))
  # d left with a left
  pair_edge(lb_map, d_11, d_21, a_21, a_11, (-1, 0), (1, 0))
  # d right as is
  # d down as is

  # e top as is
  # e left as is
  # e right with b right
  pair_edge(lb_map, e_12, e_22, b_22, b_12, (1, 0), (-1, 0))
  # e down with f right
  pair_edge(lb_map, e_21, e_22, f_12, f_22, (0, 1), (-1, 0))

  # f up as is
  # f left with a top
  pair_edge(lb_map, f_11, f_21, a_11, a_12, (-1, 0), (0, 1))
  # f right with e down
  pair_edge(lb_map, f_12, f_22, e_21, e_22, (1, 0), (0, -1))
  # f down with b top
  pair_edge(lb_map, f_21, f_22, b_11, b_12, (0, 1), (0, 1))

  # top = 11, 12
  # left = 11, 21
  # bottom = 21, 22
  # right = 12, 22

  return lb_map


def simulate(grid, instrs, start_loc, lb_map, collide=True, trace=False):
  bearings = [(1, 0), (0, 1), (-1, 0), (0, -1)]
  bearings_signature = ['>', 'v', '<', '^']
  dir_idx = 0

  loc = start_loc
  for instr in instrs:
    bearing = bearings[dir_idx]
    if instr == 'R':
      dir_idx = (dir_idx + 1) % 4 
      if trace: print('turn R to ', bearings[dir_idx])
    elif instr == 'L':
      dir_idx = (dir_idx - 1) % 4
      if trace: print('turn L to ', bearings[dir_idx])
    else:
      for i in range(instr):
        next_loc, next_bearing = get_next_loc_and_bearing(loc, bearing, lb_map)
        if trace: print('from', loc, bearing)
        if trace: print('to', next_loc, next_bearing)
        if grid.get(next_loc) == '#' and collide:
          if trace: print('interrupted')
          break
        loc, bearing = next_loc, next_bearing
        dir_idx = bearings.index(bearing)
        if loc not in grid.overlays:
          grid.overlays[loc] = bearings_signature[dir_idx]
  return loc, dir_idx

def two(INPUT):
  raw_grid, instrs = parse('\n'.join(INPUT))
  loc = (raw_grid[0].index('.'), 0)
  grid = Grid(raw_grid)
  lb_map = edges_two(grid)
  loc, dir_idx = simulate(grid, instrs, loc, lb_map)
  return 1000 * (loc[1]+1) + 4 * (loc[0] +1) + dir_idx

def test(INPUT):
  raw_grid, _ = parse('\n'.join(INPUT))
  instrs_r = [1, "R", 1, "R", 1, "R", 1]
  instrs_l = [1, "L", 1, "L", 1, "L", 1]
  grid = Grid(raw_grid)
  lb_map = edges_two(grid)
  
  for x in range(len(raw_grid[0])):
    for y in range(len(raw_grid)):
      if grid.get((x, y)) != ' ':
        start_loc = (x, y)
        loc, _ = simulate(grid, instrs_r, start_loc, lb_map, collide=False, trace=False)
        if loc != start_loc:
          # print('MISMATCH FOUND', start_loc, loc)
          grid.overlays[start_loc] = 'N'
        # else:
        #   print('SUCCESS', start_loc)
        loc, _ = simulate(grid, instrs_l, start_loc, lb_map, collide=False, trace=False)
        if loc != start_loc:
          # print('MISMATCH FOUND', start_loc, loc)
          grid.overlays[start_loc] = 'N'
        # else:
        #   print('SUCCESS', start_loc)
  # print(grid)
  return 0


if __name__ == '__main__':
  p = puzzle.Puzzle("2022", "22")

  p.run(one, 0) 
  p.run(two, 0) 
# p.run(test, 0)
