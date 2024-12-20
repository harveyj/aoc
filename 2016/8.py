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

def onetwo(INPUT):
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
          # print((x, y), (x, y_prev), G_old.get((x, y_prev)))
          G.set((x, y), G_old.get((x, y_prev)))
      else:
        y = id
        for x in range(G.max_x()):
          x_prev = x - mag
          if x_prev < 0: x_prev += G.max_x()
          G.set((x, y), G_old.get((x_prev, y)))
  #  read the letters off of this to get the answer for 2.
  for y in range(G.max_y()):
    for x in range(G.max_x()):
      print(G.get((x, y)), end='')
    print('')
  return len(G.detect('#'))

def one(INPUT):
  return onetwo(INPUT)

def two(INPUT):
  # real answer is read out of letters returned from onetwo but i want it secret
  return 'DUMMY' 

if __name__ == '__main__':
  p = puzzle.Puzzle("2016", "8")
  p.run(onetwo, 0)
