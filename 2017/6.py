#!/usr/bin/env python3
import puzzle, library
import re
import networkx as nx
import hashlib


def parse(INPUT):
  for l in INPUT:
    yield list(map(int, l.split()))


def one(INPUT):
  blocks = list(parse(INPUT))[0]
  print(blocks)
  seen = set()
  steps = 0
  while True:
    if tuple(blocks) in seen:
      return steps, blocks
    seen.add(tuple(blocks))
    steps += 1
    max_val = max(blocks)
    max_idx = blocks.index(max_val)
    blocks[max_idx] = 0
    for i in range(max_val):
      idx = (max_idx + 1 + i) % len(blocks)
      blocks[idx] += 1


def two(INPUT):
  _, blocks = one(INPUT)
  blocks = [str(b) for b in blocks]
  steps2, _ = one([' '.join(blocks)])
  return steps2

p = puzzle.Puzzle("2017", "6")
p.run(one, 0)
p.run(two, 0)
