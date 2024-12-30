#!/usr/bin/env python3
import puzzle, re, library
from collections import defaultdict
import networkx as nx
import itertools, operator
import copy

def power(x, y, sn):
  rid = x+10
  pow = rid * y
  pow += sn
  pow = pow * rid
  digit = pow // 100 % 10
  return digit - 5

def pow_grid(x, y, sn, width=3):
  tot = 0
  for dx in range(min(width, 300-width)):
    for dy in range(min(width, 300-width)):
      tot += power(x+dx, y+dy, sn)
  return tot

def one(INPUT):
  sn = int(INPUT[0])
  max_pow = 0
  loc = None
  for x in range(1, 297):
    for y in range(1, 297):
      if pow_grid(x, y, sn) > max_pow:
        max_pow =  pow_grid(x, y, sn) 
        loc = (x, y)
  return loc

def pow_grid2(sums, x, y, width=3):
  max_x = x+width-1; max_y = y+width-1
  return sums[(max_x, max_y)] + sums[(x-1, y-1)] - sums[(x-1, max_y)] - sums[(max_x, y-1)]

def onetwo_fast(INPUT, two=False):
  sn = int(INPUT[0])
  max_pow = 0
  loc = None
  grid = [[power(x, y, sn) for y in range(0, 330)] for x in range(0, 330)]
  xsums = [list(itertools.accumulate(row, operator.add)) for row in grid]
  sumgrid = {}
  for x in range(0, len(grid)):
    tot = 0
    for y in range(0, len(grid[0])):
      tot += xsums[y][x]
      sumgrid[(y, x)] = tot
  max_pow = 0
  loc = None
  for x in range(1, 300):
    for y in range(1, 300):
      if pow_grid2(sumgrid, x, y) != pow_grid(x, y, sn):
        print('mismatch', (x, y))
      rg = range(min(300-x, 300-y)) if two else [3]
      for i in rg:
        if pow_grid2(sumgrid, x, y, width=i) > max_pow:
          max_pow = pow_grid2(sumgrid, x, y, width=i) 
          loc = (x, y, i)
  return loc

one = lambda INPUT: onetwo_fast(INPUT)
two = lambda INPUT: onetwo_fast(INPUT, two=True)

if __name__ == '__main__':
  p = puzzle.Puzzle("2018", "11")
  print(p.run(one, 0))
  print(p.run(two, 0))