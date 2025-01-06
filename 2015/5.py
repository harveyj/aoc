#!/usr/bin/env python3
import puzzle
import string
import re

def is_nice(inval):
  for val in ['ab', 'cd', 'pq', 'xy']:
    if inval.count(val) > 0:
      return False

  double_counts = [inval.count(c+c) for c in string.ascii_lowercase]
  val_counts = [inval.count(c) for c in ['a', 'e', 'i', 'o', 'u']]
  return sum(val_counts) >= 3 and sum(double_counts) > 0

def one(INPUT):
  return len([l for l in INPUT if is_nice(l)])

def is_nice2(inval):
  repeat = re.search(r'(..).*\1', inval)
  sandwich = re.search(r'(.).\1', inval)
  return repeat != None and sandwich != None

def two(INPUT):
  return len([l for l in INPUT if is_nice2(l)])

if __name__ == '__main__':
  p = puzzle.Puzzle("2015", "5")

  p.run(one, 0)
  p.run(two, 0)
