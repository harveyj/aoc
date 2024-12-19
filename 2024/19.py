#!/usr/bin/env python3
import puzzle, re, library
from collections import defaultdict
from functools import lru_cache

def parse_input(INPUT):
  towels, patterns = '\n'.join(INPUT).split('\n\n')
  towels = towels.split(', ')
  patterns = patterns.split('\n')
  return towels, patterns

def one(INPUT):
  towels, patterns = parse_input(INPUT)
  pat = f"^({'|'.join([f'({t})' for t in towels])})*$"
  return len([p for p in patterns if re.fullmatch(pat, p)])


@lru_cache(maxsize=None) 
def all_matches2(towels, pattern):
  tot = 0
  for t in towels:
    if pattern == t:
      tot += 1
      continue
    if pattern[:len(t)] == t:
      tot += all_matches2(towels, pattern[len(t):])
  return tot

def two(INPUT):
  towels, patterns = parse_input(INPUT)
  out = 0
  for p in patterns:
    match = all_matches2(tuple(towels), p.strip())
    out += match
  return out

# 8:43 - 8:54
# 9:00ish - 9:29

if __name__ == '__main__':
  p = puzzle.Puzzle("2024", "19")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')
