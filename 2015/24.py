#!/usr/bin/env python3
import puzzle
import re
import networkx as nx
import itertools
import operator, functools

def parse(INPUT):
  return list(map(int, INPUT))

def qe(vals):
  return functools.reduce(operator.mul, vals)

def onetwo(INPUT, two=True):
  BINS = 4 if two else 3
  vals = parse(INPUT); tgt = sum(vals)/BINS
  max_len = len(vals)//BINS
  ideal = 10000000000000000000000000
  for i in range(max_len):
    for c in itertools.combinations(vals, i):
      if sum(c) == tgt:
        if qe(c) < ideal: ideal = qe(c)
  return ideal

def one(INPUT): return onetwo(INPUT, two=False)
def two(INPUT): return onetwo(INPUT, two=True)

p = puzzle.Puzzle("2015", "24")
p.run(one, 0)
p.run(two, 0)
