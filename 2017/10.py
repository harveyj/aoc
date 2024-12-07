#!/usr/bin/env python3
import puzzle, library
import itertools, operator

# Hat tip https://www.reddit.com/r/adventofcode/comments/7irzg5/comment/dr10ayw/

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
  ret = ''
  for val in vals:
    ret += hexchr(val // 16) + hexchr(val % 16)
  return ret

def two(INPUT):
  INPUT=INPUT[0]
  # INPUT=''
  key = list(map(ord, INPUT)) + [17, 31, 73, 47, 23]
  vals = list(range(256))
  offset = 0; skip_size = 0
  for i in range(64):
    # print(len(vals))
    _, vals, offset, skip_size = knothash(vals, key, skip_size, offset)
    print(offset, skip_size)
  print(vals)
  dense = []
  for i in range(len(vals) // 16):
    val = 0
    dense.append(list(itertools.accumulate(vals[i*16:(i+1)*16], operator.xor))[-1])
  print(list(dense))
  out = print_hex(dense)
  # print_hex([64, 7, 255])
  return out

if __name__ == '__main__':
  p = puzzle.Puzzle("2017", "10")

  p.run(one, 0)
  p.run(two, 0)
