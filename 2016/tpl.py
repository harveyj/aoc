#!/usr/bin/env python3
import puzzle
import re
import networkx as nx

def parse(INPUT):
  pat = re.compile('(\w+)+')
  for l in INPUT.split('\n'):
    yield re.match(pat, l).groups()


def one(INPUT):
  print(parse(INPUT))
  return 0

def two(INPUT):
  return 0

p = puzzle.Puzzle("13")
p.run(one, 0)
p.run(two, 0)
