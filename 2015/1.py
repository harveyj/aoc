#!/usr/bin/env python3
import puzzle

def one(INPUT):
  return INPUT[0].count('(') - INPUT[0].count(')')

def two(INPUT):
  floor = 0
  for i, c in enumerate(INPUT[0]):
    if c == '(': floor += 1
    if c == ')': floor -= 1
    if floor < 0:
      return i+1

if __name__ == '__main__':
  p = puzzle.Puzzle("2015", "1")

  p.run(one, 0)
  p.run(two, 0)