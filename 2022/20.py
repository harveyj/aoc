#!/usr/bin/env python3
import puzzle
import re
import networkx as nx

def parse(INPUT):
  return [int(i) for i in INPUT]

def mix(arr, iters=1):
  annotated = [(i, 0) for i in arr]
  iters_complete = 0
  while iters_complete < iters:
    iters_complete += 1
    idx = 0
    for _ in range(len(annotated)):
      # print('trying to move', idx)
      while annotated[idx][1] == iters_complete:
        # print('skip', idx)
        idx += 1
      val = annotated[idx][0]  
      del(annotated[idx])
      new_loc = (idx + val) % len(annotated)
      if new_loc == 0 and val != 0: new_loc = len(annotated)
      annotated.insert(new_loc, (val, iters_complete))
      # print([a[0] for a in annotated])
  return [a[0] for a in annotated]
  
def mix2(arr, iters=10):
  annotated = [(item, i, 0) for i, item in enumerate(arr)]
  iters_complete = 0
  while iters_complete < iters:
    iters_complete += 1
    # print('iter', annotated)
    for key_idx in range(len(annotated)):
      idx = 0
      while annotated[idx][1] != key_idx:
        idx += 1
      val = annotated[idx][0]
      del(annotated[idx])
      new_loc = (idx + val) % len(annotated)
      if new_loc == 0 and val != 0: new_loc = len(annotated)
      # print('moving', val, 'which is', key_idx, 'to', new_loc)
      annotated.insert(new_loc, (val, key_idx, iters_complete))
  return [a[0] for a in annotated]

def one(INPUT):
  arr = parse(INPUT)
  arr = mix(arr)
  return arr[(arr.index(0) + 1000) % len(arr)] + arr[(arr.index(0) + 2000) % len(arr)] + arr[(arr.index(0) + 3000) % len(arr)]

def two(INPUT):
  arr = parse(INPUT)
  arr = [a * 811589153 for a in arr]
  # print(arr)
  for i in range(1, 11):
    new_arr = mix2(arr, iters=i)
    # print(new_arr)
  arr = new_arr
  # print(arr[(arr.index(0) + 1000) % len(arr)], arr[(arr.index(0) + 2000) % len(arr)], arr[(arr.index(0) + 3000) % len(arr)])
  return arr[(arr.index(0) + 1000) % len(arr)] + arr[(arr.index(0) + 2000) % len(arr)] + arr[(arr.index(0) + 3000) % len(arr)]

if __name__ == '__main__':
  p = puzzle.Puzzle("2022", "20")

  p.run(one, 0) 
  p.run(two, 0) 
