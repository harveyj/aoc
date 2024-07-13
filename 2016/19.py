#!/usr/bin/env python3
import puzzle

def one(INPUT):
  num = int(INPUT[0])
  total = num
  offset = 1
  first_one = 0
  while total > 2:
    even = total % 2 == 0
    if even:
      total //= 2
    else:
      total = (total -1) // 2
      first_one += 2 * offset
    offset *= 2

  return first_one + 1 # one-based system

def two(INPUT):
  items = list(range(1, int(INPUT[0])+1))
  idx = 0
  while len(items) > 1:
    tgt = (idx + len(items) // 2)
    tgt %= len(items)
    if items[tgt] > items[idx]:
      idx += 1
    del items[tgt]
    idx %= len (items)
  return items[0]

p = puzzle.Puzzle("2016","19")
p.run(one, 0)
p.run(two, 0)
