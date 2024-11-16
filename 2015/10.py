#!/usr/bin/env python3
import puzzle

def iter(INPUT):
  i = 0
  out = []
  while i < len(INPUT):
    cur = INPUT[i]
    j = i + 1
    while j < len(INPUT) and INPUT[j] == cur:
      j += 1
    out.append((j-i, cur))
    i = j
  return ''.join([str(a) + b for a, b in out])

def one(INPUT):
  val = INPUT[0]
  for i in range(40):
    val = iter(val)
  return len(val)

def two(INPUT):
  val = INPUT[0]
  for i in range(50):
    val = iter(val)
  return len(val)

p = puzzle.Puzzle("2015", "10")
p.run(one, 0)
p.run(two, 0)
