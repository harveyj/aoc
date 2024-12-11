#!/usr/bin/env python3
import puzzle, re, library

def parse_input(INPUT):
  return [library.Grid(raw=chunk) for chunk in '\n'.join(INPUT).split('\n\n')]


def one(INPUT):
  grids = parse_input(INPUT)
  out = 0

  for G in grids:
    rows = [[G.get((x, y)) for x in range(G.max_x())] for y in range(G.max_y())]
    cols = [[G.get((x, y)) for y in range(G.max_y())] for x in range(G.max_x())]
    mirror_row = 0; mirror_col = 0
    # for r in rows: print(r)
    # for c in cols: print(c)
    for y in range(0, len(rows)-1):
      # print(rows[y+1::-1])
      pairs = list(zip(rows[y::-1], rows[y+1:]))
      mismatch = list(filter(lambda a: a[0] != a[1], pairs))
      if len(mismatch) == 0:
        mirror_row = y+1
    for x in range(0, len(cols)-1):
      pairs = list(zip(cols[x::-1], cols[x+1:]))
      mismatch = list(filter(lambda a: a[0] != a[1], pairs))

      if len(mismatch) == 0:
        mirror_col = x+1

    if mirror_row : G.overlays={(0, mirror_row): 'v', (0, mirror_row + 1):'^'}
    if mirror_col : G.overlays={(mirror_col, 0):'>', (mirror_col + 1, 0): '<'}
    # print(G)
    # print('')
    out+=(mirror_row*100+ mirror_col)
  return out

def two(INPUT):
  grids = parse_input(INPUT)
  out = 0

  for G in grids:
    rows = [[G.get((x, y)) for x in range(G.max_x())] for y in range(G.max_y())]
    cols = [[G.get((x, y)) for y in range(G.max_y())] for x in range(G.max_x())]
    mirror_row = 0; mirror_col = 0
    for y in range(0, len(rows)-1):
      pairs = list(zip(rows[y::-1], rows[y+1:]))
      zipped_pairs = [list(zip(p[0], p[1])) for p in pairs]
      total = 0
      for zp in zipped_pairs:
        comps = [1 if a != b else 0 for a, b in zp]
        total += sum(comps)
      if total == 1: 
        mirror_row = y+1
    for x in range(0, len(cols)-1):
      pairs = list(zip(cols[x::-1], cols[x+1:]))
      zipped_pairs = [list(zip(p[0], p[1])) for p in pairs]
      total = 0
      for zp in zipped_pairs:
        comps = [1 if a != b else 0 for a, b in zp]
        total += sum(comps)
      if total == 1: 
        mirror_col = x+1

    if mirror_row : G.overlays={(0, mirror_row): 'v', (0, mirror_row + 1):'^'}
    if mirror_col : G.overlays={(mirror_col, 0):'>', (mirror_col + 1, 0): '<'}
    # print(G)
    # print('')
    out+=(mirror_row*100+ mirror_col)
  return out

if __name__ == '__main__':
  p = puzzle.Puzzle("2023", "13")

  p.run(one, 0) 
  p.run(two, 0) 
