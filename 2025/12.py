#!/usr/bin/env python3
import puzzle, library

def parse_input(INPUT):
  return '\n'.join(INPUT).split('\n\n')

def one(INPUT):
  invals = parse_input(INPUT)
  blocks = invals[:-1]
  grids = invals[-1].split('\n')
  counts = []
  for b in blocks:
    lines = b.split('\n')
    raw = ''.join(lines[1:])
    counts.append(raw.count('#'))
  tot = 0
  for g in grids:
    x, y = library.ints(g)[:2]
    total_grids = library.ints(g)[2:]
    tr = sum([tg * count for tg, count in zip(total_grids, counts)])
    tp = x*y
    if tp - tr  > 10: tot += 1
  return tot

def two(INPUT):
  return 20251225

if __name__ == '__main__':
  p = puzzle.Puzzle("2025", "12")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')
