#!/usr/bin/env python3
import puzzle
import re

def parse(INPUT):
  pat = re.compile('(\w+): (\d+),? ?')
  for l in INPUT:
    yield re.findall(pat, l)

answer_sue ={ 'children': 3,
 'cats': 7,
 'samoyeds': 2,
 'pomeranians': 3,
 'akitas': 0,
 'vizslas': 0,
 'goldfish': 5,
 'trees': 3,
 'cars': 2,
 'perfumes': 1
}

def onetwo(INPUT, two=False):
  sues = list(parse(INPUT))
  for i, s in enumerate(sues):
    items = dict(s)
    found = True
    for k, v in items.items():
      v = int(v)
      if two and k in ['cats', 'trees']:
        if v < answer_sue[k]:
          found = False
          break
      elif two and k in ['pomeranians', 'goldfish']:
        if v > answer_sue[k]:
          found = False
          break
      elif v != answer_sue[k]:
        found = False
        break
    if found:
      return i+1
  return 0

def one(INPUT):
  return onetwo(INPUT, two=False)

def two(INPUT):
  return onetwo(INPUT, two=True)

if __name__ == '__main__':
  p = puzzle.Puzzle("2015", "16")

  p.run(one, 0)
  p.run(two, 0)
