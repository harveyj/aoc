#!/usr/bin/env python3
import puzzle, collections

def one(INPUT):
  # prevent bug where string wraps around because - never exists in input
  polymer = collections.deque(list(INPUT[0]+'-'))
  clean = 0
  while True:
    if polymer[0].upper() == polymer[1].upper() and polymer[0] != polymer[1]:
      clean = 0
      polymer.popleft(); polymer.popleft()
    else:
      clean += 1
      polymer.rotate(1)
    if clean == len(polymer): break
  return len(polymer) - 1

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