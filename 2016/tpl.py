#!/usr/bin/env python3
import puzzle, library
import re
import networkx as nx
import hashlib


def parse(INPUT):
  pat = re.compile('(\w+)+')
  for l in INPUT:
    yield re.match(pat, l).groups()


def one(INPUT):
  print(parse(INPUT))
  return 0

def two(INPUT):
  return 0

if __name__ == '__main__':
  p = puzzle.Puzzle("2016", "0")

  p.run(one, 0)
  p.run(two, 0)
