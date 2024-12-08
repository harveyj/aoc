#!/usr/bin/env python3
import puzzle, re, library
from collections import defaultdict


def parse_input(INPUT):
  return INPUT

def one(INPUT):
  invals = parse_input(INPUT)
  out = 0
  return out

def two(INPUT):
  invals = parse_input(INPUT)
  out = 0
  return out


  # G = puzzle.Grid(raw='\n'.join(INPUT))
  # for x in range(G.max_x()):
  #   for y in range(G.max_y()):
  #     c = G.get((x, y))

p = puzzle.Puzzle("")
p.run(one, 0)
p.run(two, 0)
