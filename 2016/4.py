#!/usr/bin/env python3
import puzzle
import re
from collections import defaultdict

def parse(INPUT):
  pat = re.compile('((\w+-)+)(\d+)\[(\w+)\]')
  for l in INPUT:
    yield re.match(pat, l).groups()


def check(code):
  name = code[:-3][0]
  checksum = code[-1]
  hist = defaultdict(int)
  for c in name:
    if c != '-':
      hist[c] += 1
  top_items = sorted(hist.items(), key=lambda k: (k[1], -ord(k[0])))[::-1][:5]
  keys = [item[0] for item in top_items]
  # print(keys)
  for k in keys:
    if k not in checksum:
      # print(f'{code} {k} not found')
      return False
  return True

def one(INPUT):
  cksum = 0
  for code in list(parse(INPUT)):
    if check(code):
      cksum += int(code[-2])
      # print(code, code[-2])
  return cksum

def two(INPUT):
  for code in list(parse(INPUT)):
    id = int(code[-2])
    decoded = ''.join([chr(((ord(c) - ord('a')) + id) % 26 + ord('a'))  for c in code[0]])
    if 'north' in decoded:
      return id

if __name__ == '__main__':
  p = puzzle.Puzzle("2016", "4")

  p.run(one, 0)
  p.run(two, 0)
