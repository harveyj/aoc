#!/usr/bin/env python3
import puzzle
import re
import networkx as nx
import math

def parse(INPUT):
  return INPUT

def translate(c):
  if c == '=': return -2
  if c == '-': return -1
  return int(c)

def rev(c):
  if c == -2: return '='
  if c == -1: return '-'
  return str(c)

def snafu(num):
  max = math.ceil(math.log(num, 5))
  vals = []
  tgt = num
  for pow in range(max, -1, -1):
    for val in [2, 1, 0, -1, -2]:
      contrib = val * (5 ** pow)
      # 2*25 + 2*5 + 2*1
      bound = sum([2 * 5**p_1 for p_1 in range(pow)])
      # print(contrib, tgt-contrib, bound, -bound <= tgt - contrib <= bound, val, pow)
      if -bound <= tgt - contrib <= bound:
        vals.append(val)
        tgt -= val * 5 ** pow
        break
  ret = []
  # print(vals)
  for val in vals:
    ret.append(rev(val))
  return ''.join(ret)

def one(INPUT):
  sum = 0
  for l in parse(INPUT):
    num = 0
    pow = 1
    for c in l[::-1]:
      num += translate(c)*pow
      pow *= 5
    # print(num)
    sum += num
  # print(sum)
  # print(snafu(sum))
  # 625 -250 -25 + 5 - 2
  print(snafu(353))
  return 0

def two(INPUT):
  print("Merry Christmas!")
  return 20221225

if __name__ == '__main__':
  p = puzzle.Puzzle("2022", "25")

  p.run(one, 0) 
  p.run(two, 0) 
