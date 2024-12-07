#!/usr/bin/env python3
import puzzle, re

def parse_input(INPUT):
  return INPUT

def one(INPUT):
  out = 0
  for chunk in INPUT:
    out += eval(chunk)
  return out

def two(INPUT):
  out = 0
  seen = set()
  while True:
    for chunk in INPUT:
      out += eval(chunk)
      if out in seen:
        return out
      seen.add(out)

if __name__ == '__main__':
  p = puzzle.Puzzle("2018", "1")

  p.run(one, 0)
  p.run(two, 0)
