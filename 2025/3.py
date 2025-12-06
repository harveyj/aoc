#!/usr/bin/env python3
import puzzle
from functools import lru_cache

def one(INPUT):
  out = 0
  for l in INPUT:
    vals = list(map(int, list(l)))
    max_val = max(vals[:-1])
    max_idx = vals.index(max_val)
    del vals[:max_idx+1]
    max_val_2 = max(vals)
    out += max_val * 10 + max_val_2
  return out

# MEMOIZEEEEE
@lru_cache(maxsize=None)
def max_joltage(bank, remaining):
  if remaining > len(bank): return 0
  if remaining == 1: return max(bank)
  include_val = int(str(bank[0]) + str(max_joltage(bank[1:], remaining - 1)))
  exclude_val = max_joltage(bank[1:], remaining)
  return max(include_val, exclude_val)

def two(INPUT):
  out = 0
  for l in INPUT:
    vals = tuple(map(int, list(l)))
    out += max_joltage(vals, 12)
  return out


if __name__ == '__main__':
  p = puzzle.Puzzle("2025", "3")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')
