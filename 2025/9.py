#!/usr/bin/env python3
import puzzle, library
import shapely

def parse_input(INPUT):
  return [list(library.ints(l)) for l in INPUT]

def one(INPUT):
  invals = parse_input(INPUT)
  print(invals)
  vals = []
  for i, a in enumerate(invals):
    for j, b in enumerate(invals[i+1:]):
      vals.append(size(a, b))
  return max(vals)

def size(a, b):
  return (abs(a[0]-b[0])+1) * (abs(a[1]-b[1]) +1)

def maxes(loc_a, loc_b):
  max_x = max(loc_a[0], loc_b[0])
  max_y = max(loc_a[1], loc_b[1])
  min_x = min(loc_a[0], loc_b[0])
  min_y = min(loc_a[1], loc_b[1])
  return (min_x, min_y, max_x, max_y)

def two(INPUT):
  invals = parse_input(INPUT)
  invals_adj = [(iv[0] + 0.5, iv[1] + 0.5) for iv in invals]

  path = shapely.Polygon(invals_adj)
  path = path.buffer(0.5, join_style=2, cap_style=3)
  candidates = []

  for i, a in enumerate(invals):
    for j, b in enumerate(invals[i+1:]):
     candidates.append((size(a, b), a, b))
  candidates = sorted(candidates, reverse=True)

  for _, a, b in candidates:
    min_x, min_y, max_x, max_y = maxes(a, b)
    rect = shapely.Polygon([(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)])
    if path.covers(rect):
      return size(a, b), a, b

if __name__ == '__main__':
  p = puzzle.Puzzle("2025", "9")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')
