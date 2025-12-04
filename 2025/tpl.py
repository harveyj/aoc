#!/usr/bin/env python3
import puzzle, re, library
from collections import defaultdict
import networkx as nx

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


  # G = library.Grid(raw='\n'.join(INPUT))
  # for x in range(G.max_x()):
  #   for y in range(G.max_y()):
  #     c = G.get((x, y))

if __name__ == '__main__':
  p = puzzle.Puzzle("2025", "")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')
