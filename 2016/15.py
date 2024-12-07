#!/usr/bin/env python3
import puzzle
import re

def parse(INPUT):
  pat = re.compile('(\w+)+')
  for l in INPUT.split('\n'):
    yield re.match(pat, l).groups()

discs_one=[
(13, 10),
(17, 15),
(19, 17),
(7, 1),
(5, 0),
(3, 1),
]

discs_two=[
(13, 10),
(17, 15),
(19, 17),
(7, 1),
(5, 0),
(3, 1),
(11, 0)
]

def legal_time(t, discs):
  for depth, d in enumerate(discs):
    period, t0_loc = d
    if (t + depth + t0_loc + 1) % period != 0:
      return False
  return True

def one(INPUT, two=False):
  discs = discs_two if two else discs_one
  for t in range(10000000):
    if legal_time(t, discs):
      return t

def two(INPUT):
  return one(INPUT, two=True)

if __name__ == '__main__':
  p = puzzle.Puzzle("2016", "15")

  p.run(one, 0)
  p.run(two, 0)
