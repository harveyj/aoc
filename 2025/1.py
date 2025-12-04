#!/usr/bin/env python3
import puzzle

def parse_input(INPUT):
  return [(-1 if a[0] == "L" else 1) * int(a[1:]) for a in INPUT]

def one(INPUT):
  invals = parse_input(INPUT)
  val = 50
  out = 0
  for rot in invals:
    val += rot
    val %= 100
    if val == 0:
      out += 1
  return out

# TODO why didn't my nice soln work
def two(INPUT):
  invals = parse_input(INPUT)
  val = 50
  out = 0
  for rot in invals:
    step = rot / abs(rot)
    while rot != 0:
      val += step
      rot -= step
      val %= 100
      if val == 0: out += 1
  return out

if __name__ == '__main__':
  p = puzzle.Puzzle("2025", "1")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')
