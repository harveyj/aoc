#!/usr/bin/env python3
import puzzle, library

def parse_input(INPUT):
  return [library.ints(l) for l in INPUT]

def check(row):
  asc = True; desc = True; adj = True
  for a1, a2 in zip(row, row[1:]):
    if a1 >= a2: asc = False
  for a1, a2 in zip(row, row[1:]):
    if a1 <= a2: desc = False
  for a1, a2 in zip(row, row[1:]):
    if not 1 <= abs(a1 - a2) <= 3:
      adj = False
  return (asc or desc) and adj

def one(INPUT):
  invals = parse_input(INPUT)
  good_rows = [row for row in invals if check(row)]
  return len(good_rows)

def two(INPUT):
  invals = parse_input(INPUT)
  good = set()
  for row in invals:
    if check(row):
      good.add(tuple(row))
    else:
      for i in range(len(row)):
        new_row = row[:i] + row[i+1:]
        if check(new_row):
          good.add(tuple(row))
  return len(good)

if __name__ == '__main__':
  p = puzzle.Puzzle("2024", "2")

  p.run(one, 0)
  p.run(two, 0)
