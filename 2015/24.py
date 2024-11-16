#!/usr/bin/env python3
import puzzle
import re
import networkx as nx
import itertools
import operator, functools

def parse(INPUT):
  return list(map(int, INPUT.split('\n')))

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
        print(c, qe(c))
  return ideal

def two(INPUT):
  return 0

p = puzzle.Puzzle("2015", "24")
p.run(onetwo, 0)
