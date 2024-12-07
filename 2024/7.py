#!/usr/bin/env python3
import puzzle, re, itertools
from library import ints
import operator

def parse_input(INPUT):
  for l in INPUT:
    yield ints(l)[0], ints(l)[1:]

def concat(a, b):
  return int(str(a)+str(b))

def puzz(INPUT, two = False):
  out = 0
  opers = [operator.mul, operator.add, concat] if two else [operator.mul, operator.add]
  for lval, rvals in parse_input(INPUT):
    for ops in itertools.product(opers, repeat=len(rvals)-1):
      total = rvals[0]
      for op, rval in zip(ops, rvals[1:]):
        total = op(total, rval)
      if total == lval:
        out += lval
        break
  return out

def one(INPUT):
  return puzz(INPUT)

def two(INPUT):
  return puzz(INPUT, two=True)

if __name__ == '__main__':
  p = puzzle.Puzzle("2024", "7")
  p.run(one, 0)
  p.run(two, 0)
