#!/usr/bin/env python3
import puzzle

def one(INPUT):
  twos = []; threes = []
  for l in INPUT:
    counts = [l.count(c) for c in set(l)]
    if 2 in counts:
      twos.append(l)
    if 3 in counts: 
      threes.append(l)
  return len(twos) * len(threes)

def two(INPUT):
  seen = []
  for l in INPUT:
    for s in seen:
      diff = 0
      for c1, c2 in zip(l, s): 
        if c1 != c2:
          diff += 1
      if diff == 1:
        return ''.join([c1 for c1, c2 in zip(l, s) if c1 == c2])
    seen.append(l)

p = puzzle.Puzzle("2018", "2")
p.run(one, 0)
p.run(two, 0)
