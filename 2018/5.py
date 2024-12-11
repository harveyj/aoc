#!/usr/bin/env python3
import puzzle

def one(INPUT):
  polymer = list(INPUT[0])
  dirty = True
  while dirty:
    dirty = False
    i = 0
    while i < len(polymer) - 1:
      if ((polymer[i].upper() == polymer[i+1]) or (polymer[i].lower() == polymer[i+1])) and (polymer[i] != polymer[i+1]):
        del polymer[i:i+2]
        dirty = True
      i += 1
  return len(polymer)

def two(INPUT):
  polymer = list(INPUT[0])
  vals = []
  for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    new_poly = [ch for ch in polymer if ch not in [c.lower(), c.upper()]]
    vals.append(one([''.join(new_poly)]))
  return min(vals)

if __name__ == '__main__':
  p = puzzle.Puzzle("2018", "5")
  print(p.run(one, 0))
  print(p.run(two, 0))