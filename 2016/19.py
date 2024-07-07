#!/usr/bin/env python3
import puzzle, library
import re
import networkx as nx
import hashlib



def one(INPUT):
  num = int(INPUT[0])
  total = num
  offset = 1
  first_one = 0
  while total > 2:
    # print(total)
    even = total % 2 == 0
    if even:
      total //= 2
    else:
      total = (total -1) // 2
      first_one += 2 * offset
    offset *= 2
    print(f't {total}, o {offset}, fo {first_one}')

  return first_one + 1 # one-based system

def two(INPUT):
  items = list(range(1, int(INPUT[0])+1))
  idx = 0
  while len(items) > 1:
    tgt = (idx + len(items) // 2)
    # print(f'idx {idx} elf {items[idx]} tgt {tgt} li {len(items)}')
    # if tgt == len(items): tgt = len(items) -1
    tgt %= len(items)
    if items[tgt] > items[idx]:
      idx += 1
    else: pass
    # print('deleting', items[tgt])
    del items[tgt]
    idx %= len (items)
  return items[0]

p = puzzle.Puzzle("19")
# p.run(one, 0)
p.run(two, 0)
