#!/usr/bin/env python3
import puzzle
import hashlib
import itertools

def next_char(INPUT, two=False):
  for i in range(1000000000):
    hashval = hashlib.md5((INPUT+str(i)).encode('utf-8')).hexdigest()
    if hashval[:5] == '00000':
      yield (hashval[5], hashval[6]) if two else hashval[5]
  return -1

def one(INPUT):
  chars = next_char('wtnhxymk')
  return ''.join(list(itertools.islice(chars, 8)))

def two(INPUT):
  chars = next_char('wtnhxymk', two=True)
  char_list = list(itertools.islice(chars, 30))
  # print(char_list)
  passw = [0] * 8
  for i in range(8):
    for (char, val) in char_list:
      if char == str(i):
        passw[i] = val
        break
  # print(passw)
  return ''.join(passw)

p = puzzle.Puzzle("2016", "5")
p.run(one, 0)
p.run(two, 0)