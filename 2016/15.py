#!/usr/bin/env python3
import puzzle
import re
import networkx as nx

def parse(INPUT):
  pat = re.compile('(\w+)+')
  for l in INPUT.split('\n'):
    yield re.match(pat, l).groups()

discs=[
(13, 10),
(17, 15),
(19, 17),
(7, 1),
(5, 0),
(3, 1),
]

discs=[
(13, 10),
(17, 15),
(19, 17),
(7, 1),
(5, 0),
(3, 1),
(11, 0)
]


# discs=[(5, 4), (2, 1)]


def legal_time(t):
  for depth, d in enumerate(discs):
    period, t0_loc = d
    # (t0_loc + depth + 1) % period = 0 
    # (t0_loc + depth + 1) = period
    if (t + depth + t0_loc + 1) % period != 0:
      return False
  return True
    # print(f'you can drop off at time {(period - t0_loc - depth - 1)} + n * {period}')

def one(INPUT):
  # offset = 1; total_period = 1
  # for d in discs:
  #   period, t0_loc = d
  #   loc = (t0_loc + offset) % period
  #   while loc != 0:
  #     loc += total_period
  #     loc %= period
  #     offset += total_period
  #   print(f'you can drop at off')
  #   offset += 1 # it takes t=1 duration to fall through no matter what
  #   total_period *= period
  #   total_period += 1
  #   print(total_period, offset)

  for t in range(10000000):
    if legal_time(t):
      return t


p = puzzle.Puzzle("15")
p.run(one, 0)
