#!/usr/bin/env python3
import puzzle, library

def parse_input(INPUT):
  for l in INPUT: yield library.ints(l)

def one(INPUT):
  boxes = list(parse_input(INPUT))
  seen = set()
  double_seen = set()
  for id, x1, y1, w, h in boxes:
    for x in range(x1, x1+w):
      for y in range(y1, y1+h):
        if (x, y) in seen:
          double_seen.add((x, y))
        seen.add((x, y))
  return len(double_seen)

def two(INPUT):
  boxes = list(parse_input(INPUT))
  G = library.Grid(1000, 1000)
  bad_ids = set()
  for id, x1, y1, w, h in boxes:
    for x in range(x1, x1+w):
      for y in range(y1, y1+h):
        if G.get((x, y)) != '.':
          bad_ids.add(id)
          bad_ids.add(G.get((x, y)))
        G.set((x, y), id)
  return [id for id in range(1, len(INPUT)) if id not in bad_ids][0]

if __name__ == '__main__':
  p = puzzle.Puzzle("2018", "3")

  p.run(one, 0)
  p.run(two, 0)
