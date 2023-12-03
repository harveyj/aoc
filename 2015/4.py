#!/usr/bin/env python3
import puzzle
import hashlib

def parse(INPUT):
  return 0

def one(INPUT):
  for i in range(10000000):
    if hashlib.md5((INPUT+str(i)).encode('utf-8')).hexdigest()[:6] == '000000':
      return i
  return -1

def two(INPUT):
  # one and two were just 5 and 6 digits
  return 0

p = puzzle.Puzzle("4")
p.run(one, 0)
p.run(two, 0)
