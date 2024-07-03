#!/usr/bin/env python3
import puzzle
import re
import library
import copy

def parse(INPUT):
  pat_rect = re.compile('(\w+) (\d+)x(\d+)')
  pat_rotate = re.compile('(\w+) .* ([xy])=(\d+) by (\d+)')
  for l in INPUT:
    if re.match(pat_rect, l):
      yield re.match(pat_rect, l).groups()
    else:
      yield re.match(pat_rotate, l).groups()

def one(INPUT):
  G = library.Grid(x=50, y=6)
  # G = library.Grid(x=7, y=3)
  for inst in parse(INPUT):
    G_old = library.Grid(grid=copy.deepcopy(G.grid))
    if inst[0] == 'rect':
      x, y = int(inst[1]), int(inst[2])
      for x_i in range(x):
        for y_i in range(y):
          G.set((x_i, y_i), '#')
    elif inst[0] == 'rotate':
      dim = inst[1]; id = int(inst[2]); mag = int(inst[3])
      if dim == 'x':
        x = id
        for y in range(G.max_y()):
          y_prev = y - mag
          if y_prev < 0: y_prev += G.max_y()
          print((x, y), (x, y_prev), G_old.get((x, y_prev)))
          G.set((x, y), G_old.get((x, y_prev)))
      else:
        y = id
        for x in range(G.max_x()):
          x_prev = x - mag
          if x_prev < 0: x_prev += G.max_x()
          G.set((x, y), G_old.get((x_prev, y)))
    # print(G)
    # print('')
  print(len(G.detect('#')))
  print(G)
  return 0

def two(INPUT):
  return 0

p = puzzle.Puzzle("8")
p.run(one, 0)
# p.run(two, 0)
