#!/usr/bin/env python3
import puzzle
import re

def parse(INPUT):
  pat = re.compile('(\w+)+')
  for l in INPUT.split('\n'):
    yield re.match(pat, l).groups()

def expand(a):
  b = a
  b = b[::-1]
  b = ''.join(['1' if c == '0' else '0' for c in b])
  return a + '0' + b

def checksum(data):
  sum = []
  for i in range(0, len(data), 2):
    a, b = data[i], data[i+1]
    sum.append('1' if a == b else '0')
  return ''.join(sum)

def puzz(INPUT, max_len):
  data = INPUT[0]
  while len(data) < max_len:
    data = expand(data)
  data = data[:max_len]
  cksum = checksum(data)
  while len(cksum) % 2 == 0:
    cksum = checksum(cksum)
  return cksum

def one(INPUT):
  return puzz(INPUT, max_len=272)

def two(INPUT):
  return puzz(INPUT, max_len=35651584)

p = puzzle.Puzzle("2016", "16")
p.run(one, 0)
p.run(two, 0)
