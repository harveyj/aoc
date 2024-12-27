#!/usr/bin/env python3
import puzzle, re, library
import itertools
import operator

def parse_input(INPUT):
  chunks = '\n'.join(INPUT).split('\n\n')
  # print(chunks[-1])
  keys = []; locks = []
  for chunk in chunks:
    G = library.Grid(raw=chunk)
    hist = [len(['#' for y in range(G.max_y()) if G.get((x, y)) == '#']) for x in range(G.max_x())]
    # hist = [([y for y in range(G.max_y())]) for x in range(G.max_x())]
    print(G)
    print(hist)
    if G.get((0,0)) == '#':
      keys.append(hist)
    else:
      locks.append(hist)
  return keys, locks

def one(INPUT):
  keys, locks = parse_input(INPUT)
  out = 0
  for k in keys:
    for l in locks:
      bad = [a + b > 7 for a, b in zip(k, l)]
      print(bad)
      if not list(itertools.accumulate(bad, operator.or_))[-1]:
        # print(val)
        out += 1
  return out

def two(INPUT):
  return 20241225

# 31250 too high
if __name__ == '__main__':
  p = puzzle.Puzzle("2024", "25")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')
