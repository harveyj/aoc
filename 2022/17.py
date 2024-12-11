#!/usr/bin/env python3
import puzzle
from collections import defaultdict

shapes = """####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##""".split('\n\n')
shapes = [s.split('\n') for s in shapes]

class Grid:
  def __init__(self, x, y):
    BOTTOM = y + 1
    LEFT = 0
    RIGHT = x + 1
    self.x = x + 2; self.y = BOTTOM
    # +2 and +1 account for walls
    self.grid = [["." for i in range(self.x)] for j in range(self.y+1)]
    for gx in range(self.x):
      self.set((gx, BOTTOM), '-')
    for gy in range(BOTTOM):
      self.set((LEFT, gy), '|')
      self.set((RIGHT, gy), '|')
    self.overlays = []

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

  def window(self, min_x, min_y, max_x, max_y):
    return '\n'.join([''.join(row[min_x:max_x]) for row in self.grid[min_y:max_y]])

def parse(INPUT):
  return list(INPUT)

LEFT, RIGHT = -1, 1
INPUT_MAP = {'<': LEFT, '>': RIGHT}

def try_move(grid, shape, upper, left, dx, dy):
  upper += dy
  left += dx
  for sy, row in enumerate(shape):
    for sx, cell in enumerate(row):
      if cell != '#': continue
      x = left + sx
      y = upper + sy
      if grid.get((x, y)) != '.':
        return False
  return True

def reset_grid(grid, next_shape):
  def check_row_filled(grid, y):
    for x in range(1, grid.x-1):
      if grid.get((x, y)) != '.':
        return True
    return False

  upper, left = 0, 3
  for y in range(grid.y, 0, -1):
    if not check_row_filled(grid, y):
      upper = y - 2 - len(next_shape)
      break
  return y, upper, left

def simulate(instrs):
  HEIGHT = 50000
  pc = 0
  total = 0
  cur_shape = shapes[total]
  G = Grid(7, HEIGHT)
  _, upper, left = reset_grid(G, cur_shape)
  while True:
    instr = instrs[pc % len(instrs)]
    G.overlays = {}
    for sy, row in enumerate(cur_shape):
      for sx, cell in enumerate(row):
        if cell != '#': continue
        x = left + sx
        y = upper + sy
        G.overlays[(x, y)] =  '@'

    if try_move(G, cur_shape, upper, left, INPUT_MAP[instr], 0):
      left += INPUT_MAP[instr]
      # if failed, do nothing
    if try_move(G, cur_shape, upper, left, 0, 1):
      upper += 1
    else:
      for sy, row in enumerate(cur_shape):
        for sx, cell in enumerate(row):
          if cell != '#': continue
          x = left + sx
          y = upper + sy
          G.set((x, y),  '#')
      total += 1
      cur_shape = shapes[total % 5]
      max, upper, left = reset_grid(G, cur_shape)
      yield (total, pc % len(instrs), HEIGHT - max)
    pc += 1
    # a = input()


def one(INPUT):
  instrs = parse(INPUT[0])
  for i in simulate(instrs):
    total, pc_offset, top = i
    if total == 2022:  
      return top

def two(INPUT):
  instrs = parse(INPUT[0])
  last_tops = defaultdict(int)
  last_total_shapes = defaultdict(int)

  # we are looking for a loop where pc_offset is the tame, total%5 (shape) is the same and distance increased is the same
  seen = set() # (pc_offset, delta, )
  for i in simulate(instrs):
    total_shapes, pc_offset, top = i
    shape = total_shapes % 5
    delta = top - last_tops[(pc_offset, shape)]
    delta_shapes = total_shapes - last_total_shapes[(pc_offset, shape)]
    if (pc_offset, delta, total_shapes % 5, delta_shapes) in seen:
      # print('at %i instruction and %i shape, piece %i moved upwards by as much (%i) as the previous cycle, moving up %i shapes' %(pc_offset, shape, total_shapes, delta, delta_shapes))
      if (1000000000000 - total_shapes) % delta_shapes == 0:
        rotations = (1000000000000 - total_shapes) // delta_shapes
        return delta * rotations + top
    seen.add((pc_offset, delta, total_shapes%5, delta_shapes))
    last_tops[(pc_offset, shape)]= top
    last_total_shapes[(pc_offset, shape)]= total_shapes

if __name__ == '__main__':
  p = puzzle.Puzzle("2022", "17")

  p.run(one, 0) 
  p.run(two, 0) 
