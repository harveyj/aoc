#!/usr/bin/env python3
import puzzle
import hashlib

def one(INPUT):
  for i in range(10000000):
    if hashlib.md5((INPUT[0]+str(i)).encode('utf-8')).hexdigest()[:5] == '00000':
      return i

def two(INPUT):
  for i in range(10000000):
    if hashlib.md5((INPUT[0]+str(i)).encode('utf-8')).hexdigest()[:6] == '000000':
      return i

if __name__ == '__main__':
  p = puzzle.Puzzle("2015", "4")

  p.run(one, 0)
  p.run(two, 0)
