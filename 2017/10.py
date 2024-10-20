#!/usr/bin/env python3
import puzzle, library

def parse(INPUT):
  return list(map(int, INPUT[0].split(',')))

def rotate(l, n):
  return l[n:] + l[:n]


def knothash(vals, lengths):
  skip_size = 0
  offset = 0
  for l in lengths:
    if l != 0:
      vals = rotate(vals, (offset) % len(vals))
      vals = vals[l-1::-1] + vals[l:]
      vals = rotate(vals, -((offset)% len(vals)))
    offset += l + skip_size
    skip_size += 1
  return vals[0]*vals[1]

def one(INPUT):
  return knothash(list(range(256)), parse(INPUT))

def two(INPUT):
  INPUT=INPUT[0]
  print(INPUT)
  INPUT="1,2,3"
  key = list(map(ord, INPUT)) + [17, 31, 73, 47, 23]
  print(key)
  return 0

p = puzzle.Puzzle("2017", "10")
p.run(one, 0)
p.run(two, 0)
