#!/usr/bin/env python3
import puzzle
import re
import networkx as nx

def parse(INPUT):
  return 0

def one(INPUT):
  return INPUT.count('(') - INPUT.count(')')

def two(INPUT):
  floor = 0
  for i, c in enumerate(INPUT):
    if c == '(': floor += 1
    if c == ')': floor -= 1
    if floor < 0:
      return i
p = puzzle.Puzzle("1")
p.run(one, 0)
p.run(two, 0)
