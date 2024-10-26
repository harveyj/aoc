#!/usr/bin/env python3
import puzzle
from collections import defaultdict

def rotate(l, n):
  return l[-n:] + l[:-n]

def parse(INPUT):
  return INPUT[0].split(',')

def dance(instrs, data):
  for inst in instrs:
    # print(''.join(data))
    op, vals = inst[0], inst[1:]
    if op == 's':
      data = rotate(data, int(vals))
    elif op == 'x':
      a, b = list(map(int, vals.split('/')))
      tmp = data[a]
      data[a] = data[b]
      data[b] = tmp
    elif op == 'p':
      a, b = vals.split('/')
      a_idx = data.index(a)
      b_idx = data.index(b)
      data[a_idx] = b
      data[b_idx] = a
  return data


def one(INPUT):
  instrs = parse(INPUT)
  return ''.join(dance(instrs, list("abcdefghijklmnop")))

def two(INPUT):
  instrs = parse(INPUT)
  cache = defaultdict(list)
  data = list("abcdefghijklmnop")
  for i in range(10000):
    if cache[tuple(data)] != []:
      period = i - cache[tuple(data)][0]
      if (1000000000 - i) % period == 0:
        return ''.join(data)
    cache[tuple(data)].append(i)
    data = dance(instrs, data)

p = puzzle.Puzzle("2017", "16")
p.run(one, 0)
p.run(two, 0)
