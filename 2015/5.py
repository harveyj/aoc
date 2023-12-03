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
  total = 0
  for l in INPUT.split('\n'):
    if is_nice(l):
      print('nice', l)
      total += 1
    else: print('no', l)
  return total

def is_nice2(inval):
  repeat = re.search(r'(..).*\1', inval)
  sandwich = re.search(r'(.).\1', inval)
  print(repeat, sandwich, inval)
  return repeat != None and sandwich != None

def two(INPUT):
  total = 0
  for l in INPUT.split('\n'):
    if is_nice2(l):
      print('nice', l)
      total += 1
    else: print('no', l)
  return total

p = puzzle.Puzzle("5")
p.run(one, 0)
p.run(two, 0)
