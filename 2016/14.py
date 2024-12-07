#!/usr/bin/env python3
import puzzle
import re
import hashlib
from collections import defaultdict

def md5hash(inval):
  md5_hash = hashlib.md5()
  md5_hash.update(inval.encode('utf-8'))
  return md5_hash.hexdigest()

def one(INPUT, two=False):
  salt = INPUT[0]
  triples = list() # loc, char. sorted by loc
  pentas = defaultdict(list) # key = char, val = list of penta locs
  triple_pat = re.compile(r'(\w)\1\1')
  penta_pat = re.compile(r'(\w)\1\1\1\1')
  for i in range(40000):
    hash_hex = salt+str(i)
    hashes = 2017 if two else 1
    for _ in range(hashes):
      hash_hex = md5hash(hash_hex)
    # print(i,hash_hex)
    triple_match = re.search(triple_pat, hash_hex)
    penta_match = re.search(penta_pat, hash_hex)
    if triple_match:
      triples.append((i, triple_match.group(1)))
    if penta_match:
      pentas[penta_match.group(1)].append((i))
  valid_chars = []
  for loc, char in triples:
    for penta_loc in pentas[char]:
      if penta_loc > loc and penta_loc < loc+1000:
        valid_chars.append(char)
        if len(valid_chars) == 64:
          return loc
        break
  return 0

def two(INPUT):
  return one(INPUT, two=True)

if __name__ == '__main__':
  p = puzzle.Puzzle("2016", "14")

  p.run(one, 0)
  p.run(two, 0)
