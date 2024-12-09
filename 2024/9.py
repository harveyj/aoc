#!/usr/bin/env python3
import puzzle, re, library, copy
from collections import defaultdict
from itertools import chain

def parse_input(INPUT):
  return list(map(int, INPUT))

def process(blocks, skips):
  fills = []
  skips = copy.copy(skips)
  for bid, b_size in list(blocks)[-1::-1]:
    for i in range(b_size):
      fills.append(bid)
      if skips[0] == 0: skips.pop(0)
      if not skips: 
        return fills
      skips[0] -= 1
  return fills

def checksum(out):
  return sum([a*int(b) for a, b in enumerate(out) if b != '.'])

def one(INPUT):
  items = parse_input(INPUT[0])
  blocks = list(enumerate(items[::2]))
  total = sum(items[::2])
  skips = items[1::2]
  fills = process(blocks, skips)
  fills_idx = 0
  out = []
  for block, skip in zip(blocks, skips):
    bid, bsize = block
    for i in range(bsize):
      if len(out) == total:
        return checksum(out)
      out += [bid]
    for i in range(skip):
      if len(out) == total:
        return checksum(out)
      out.append(fills[fills_idx])
      fills_idx += 1

def checksum2(out):
  ret = 0
  idx = 0
  for a, b in out:
    for i in range(b):
      if a != '.':
        ret += a * idx
      idx += 1
  return ret

def two(INPUT):
  items = parse_input(INPUT[0])
  array = [[i//2 if i % 2 == 0 else '.', size] for i, size in enumerate(items)]
  id = len(items)//2
  while id > -1:
    from_idx = 0
    # scan forward to find start of id block
    while from_idx < len(array):
      if array[from_idx][0] == id:
        break
      from_idx += 1
    to_idx = 0
    # scan forward finding where the empty span is that fits it
    while to_idx < from_idx:
      if array[to_idx][0] == '.' and array[to_idx][1] >= array[from_idx][1]:
        array[to_idx][1] -= array[from_idx][1]
        array.insert(to_idx, copy.copy(array[from_idx]))
        array[from_idx+1][0] = '.'
        break
      to_idx += 1
    # consolidate any empty spans
    idx = 0
    while idx < len(array) - 1:
      if array[idx][0] == '.' and array[idx+1] == '.':
        array[idx][1] += array[idx+1][1]
        del array[idx+1]
        continue
      idx += 1
    id -= 1
  return checksum2(array)

p = puzzle.Puzzle("2024", "9")
p.run(one, 0)
p.run(two, 0)
