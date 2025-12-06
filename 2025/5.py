#!/usr/bin/env python3
import puzzle, library

def parse_input(INPUT):
  db_raw, vals_raw = INPUT.split("\n\n")
  db_raw = db_raw.replace("-", "_")
  db = [(a[0], a[1]+1) for a in map(library.ints, db_raw.split("\n"))]
  vals = [a[0] for a in map(library.ints, vals_raw.split("\n"))]
  return db, vals

def one(INPUT):
  db, vals = parse_input("\n".join(INPUT))
  print(db, vals)
  out = 0
  for v in vals:
    for a, b in db:
      if a <= v < b: 
        out += 1
        print(v)
        break
  return out

def two(INPUT):
  db, _ = parse_input("\n".join(INPUT))
  events = sorted([(a[0], 's') for a in db] + [(a[1], 'e') for a in db])
  print(events)
  stack = []
  range_start = -1
  out = 0 
  for e in events:
    loc, code = e
    if code == 's':
      range_start = loc if stack == [] else range_start
      stack.append(loc)
    else:
      stack.pop()
      if stack == []:
        out += loc - range_start
        range_start = -1
  return out

if __name__ == '__main__':
  p = puzzle.Puzzle("2025", "5")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')
