#!/usr/bin/env python3
import puzzle, re, library
from collections import defaultdict
import networkx as nx
import itertools

def manhattan(a, b):
  return sum([abs(a[i] - b[i]) for i in range(3)])

def one(INPUT):
  bots = [library.ints(l) for l in INPUT]
  biggest_bot = max(bots, key=lambda b: b[3])
  tot = 0
  for b in bots:
    # if b == biggest_bot: continue
    if manhattan(biggest_bot, b) <= biggest_bot[3]: tot += 1
  return tot

def two(INPUT):
  out = 0
  return out

if __name__ == '__main__':
  p = puzzle.Puzzle("2018", "23")
  print(p.run(one, 0))
  print(p.run(two, 0))