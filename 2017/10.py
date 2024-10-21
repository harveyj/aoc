#!/usr/bin/env python3
import puzzle, library
import itertools, operator

def parse(INPUT):
  return list(map(int, INPUT[0].split(',')))

def rotate(l, n):
  return l[n:] + l[:n]

def knothash(vals, lengths, skip_size=0, offset=0):
  for l in lengths:
    if l != 0:
      vals = rotate(vals, (offset) % len(vals))
      vals = vals[l-1::-1] + vals[l:]
      vals = rotate(vals, -((offset)% len(vals)))
    offset += l + skip_size
    skip_size += 1
  return vals[0]*vals[1], vals, offset, skip_size

def one(INPUT):
  return knothash(list(range(256)), parse(INPUT))[0]

def hexchr(i):
  return '0123456789abcdef'[i]

def print_hex(vals):
  for val in vals:
    print(hexchr(val // 16), hexchr(val % 16))


def two(INPUT):
  INPUT=INPUT[0]
  key = list(map(ord, INPUT)) + [17, 31, 73, 47, 23]
  vals = list(range(256))
  offset = 0; skip_size = 0
  for i in range(64):
    _, vals, offset, skip_size = knothash(vals, key, offset, skip_size)
  print(vals[:16])
  val = (list(itertools.accumulate(vals[:16], operator.xor))[-1])
  print_hex([val])
  # print_hex([64, 7, 255])
  return 0

p = puzzle.Puzzle("2017", "10")
p.run(one, 0)
p.run(two, 2)
