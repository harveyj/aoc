#!/usr/bin/env python3
import puzzle


CODES = '''20151125  18749137  17289845  30943339  10071777  33511524
 31916031  21629792  16929656   7726640  15514188   4041754
 16080970   8057251   1601130   7981243  11661866  16474243
 24592653  32451966  21345942   9380097  10600672  31527494
     77061  17552253  28094349   6899651   9250759  31663883
  33071741   6796745  25397450  24659492   1534922  27995004'''

def parse(INPUT):
  return [[int(c) for c in l.split()] for l in INPUT.split('\n')]

def loc(row, col):
  idx = 1
  for i in range(row):
    idx += i
  for i in range(1,col):
    idx += row+i
  return idx

def code(idx):
  code = 20151125
  for i in range(idx):
    code *= 252533
    code %= 33554393
  return code

# TODO cleanup
def one(INPUT):
  x, y = map(int, INPUT[0].split(","))
  a = parse(CODES)
  grid = [[0] * 7, [0] * 7,[0] * 7,[0] * 7,[0] * 7,[0] * 7,[0] * 7,[0] * 7] 
  for i in range(1, 7):
    for j in range(1, 7):
      grid[i-1][j-1] = code(loc(i,j)-1)
  # print('\n'.join([str(row) for row in grid]))
  return code(loc(x, y) - 1)

if __name__ == '__main__':
  p = puzzle.Puzzle("2015", "25")
  p.run(one, 0)
  # Part two is a freebie!