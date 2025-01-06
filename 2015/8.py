#!/usr/bin/env python3
import puzzle

def parse(INPUT):
  return INPUT

def one(INPUT):
  code = 0
  str_rep = 0
  for l in parse(INPUT):
    l = l.strip()
    code += len(l)
    # lol cheating
    str_rep += len(eval(l))
  return code - str_rep

def two(INPUT):
  total = 0
  for l in parse(INPUT):
    l = l.strip()
    slash = l.count('\\')
    quote = l.count('"')
    total += slash + quote + 2
  return total


if __name__ == '__main__':
  p = puzzle.Puzzle("2015", "8")

  p.run(one, 0)
  p.run(two, 0)
