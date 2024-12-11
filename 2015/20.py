#!/usr/bin/env python3
import puzzle
import math
import sympy

def parse(INPUT):
  return int(INPUT[0])

BUFFER = 20000

def presents_one(n):
  return sum(sympy.divisors(n))

def presents_two(n):
  factors = sympy.divisors(n)
  filtered = [f for f in factors if n / f <= 50]
  return sum(filtered)

def one(INPUT, one=True):
  target = int(INPUT[0]) / (10 if one else 11)
  base = 0
  exp = 25
  prez_fn = presents_one if one else presents_two
  while exp > 13:
    low_vals = [prez_fn(base+2**(exp)-BUFFER//2 + j) for j in range(BUFFER)]
    if max(low_vals) < target:
      base += 2**(exp)
    #   print(f'update {base} {exp} {min(low_vals)} vs {target}')
    # else:
    #   print(f'miss {base} {exp} {min(low_vals)} vs {target}')
    exp -= 1
  # print('here we go ', base, exp )
  for i in range(base, base+50000):
    if prez_fn(i) > target:
      return i

def two(INPUT):
  return one(INPUT, one=False)

if __name__ == '__main__':
  p = puzzle.Puzzle("2015", "20")

  print(p.run(one, 0))
  print(p.run(two, 0))
