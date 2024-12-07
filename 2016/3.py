#!/usr/bin/env python3
import puzzle
import re
import networkx as nx

def parse(INPUT):
  pat = re.compile('(\d+)')
  for l in INPUT:
    yield list(map(int, re.findall(pat, l)))

def parse2(INPUT):
  all = [list(map(int, l.split())) for l in INPUT]
  for i in range(len(all)):
    yield all[i][0]
  for i in range(len(all)):
    yield all[i][1]
  for i in range(len(all)):
    yield all[i][2]

def one(INPUT):
  valid = 0
  invals = parse(INPUT)
  for sides in invals:
    a, b, c = sides
    if a < b+c and b < a+c and c < b+a:
      # print(a, b, c)
      valid += 1
  return valid

def two(INPUT):
  valid = 0
  invals = parse2(INPUT)
  while True:
    a, b, c = next(invals, None), next(invals, None), next(invals, None)
    if None in [a, b, c]:
      return valid
    if a < b+c and b < a+c and c < b+a:
      valid += 1

if __name__ == '__main__':
  p = puzzle.Puzzle("2016", "3")

  p.run(one, 0)
  p.run(two, 0)
