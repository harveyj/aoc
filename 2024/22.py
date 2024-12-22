#!/usr/bin/env python3
import puzzle, re, library
from collections import defaultdict
import itertools

def secret(num, iters):
  mix = lambda a, b: a^b
  prune = lambda a: a % 16777216
  deltas = []
  nums = []
  for i in range(iters):
    # Calculate the result of multiplying the secret number by 64. 
    # Then, mix this result into the secret number. Finally, prune the secret number. 
    new_num = prune(mix(num, num * 64))
    # Calculate the result of dividing the secret number by 32. Round the result
    # down to the nearest integer. 
    a = new_num // 32
    # Then, mix this result into the secret number. 
    new_num = mix(a, new_num)
    # Finally, prune the secret number. 
    new_num = prune(new_num)
    # Calculate the result of multiplying the secret number by 2048. 
    b = new_num * 2048
    # Then, mix this result into the secret number. Finally, prune the secret number.
    new_num = prune(mix(b, new_num))
    # print(i, new_num)
    deltas.append(new_num % 10 - num % 10)
    nums.append(num)
    num = new_num
  return nums, deltas

def one(INPUT):
  out = []
  for l in INPUT:
    nums, _ = secret(int(l), 2000)
    out.append(nums[-1])
  return sum(out)

def find(delts, key):
  for i in range(len(delts) - len(key)):
    print(delts[i:i+len(key)], key)
    if delts[i:i+len(key)] == key:
      return i
  return -1

def create_dict(items):
  ret = dict()
  for key, val in items:
    if key not in ret:
      ret[key] = val
  return ret

def two(INPUT):
  length = 2000
  all_nums = dict()
  all_seqs = defaultdict(list)
  all_deltas = dict()
  for l in INPUT:
    nums, deltas = secret(int(l), length)
    all_nums[l] = nums
    all_deltas[l] = deltas
    all_seqs[l] = create_dict([(tuple(deltas[i:i+4]), i) for i in range(len(deltas)-4)])

  outs = defaultdict(int)
  keys = itertools.product(range(-9, 10), repeat=4)
  for key in keys:
    if not -9 <= sum(key) <= 9:
      continue
    for source in all_nums:
      delts = all_seqs[source]
      if key in delts:
        idx = delts[key]+4 # +4 due to end of sequence
        sale = all_nums[source][idx]
        outs[key] += sale % 10
  return max(outs.values())

if __name__ == '__main__':
  p = puzzle.Puzzle("2024", "22")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')
