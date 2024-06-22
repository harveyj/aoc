#!/usr/bin/env python3
import puzzle
import re
import networkx as nx

def parse(INPUT):
  pat = re.compile('(\w+): (\d+),? ?')
  for l in INPUT.split('\n'):
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
# strip out some of the code to get to one
def onetwo(INPUT):
  sues = list(parse(INPUT))
  for i, s in enumerate(sues):
    items = dict(s)
    found = True
    for k, v in items.items():
      v = int(v)
      if k in ['cats', 'trees']:
        if v < answer_sue[k]:
          found = False
          break
      elif k in ['pomeranians', 'goldfish']:
        if v > answer_sue[k]:
          found = False
          break
      elif v != answer_sue[k]:
        found = False
        break
    if found: print(i+1)
    # print(i+1, items)
  return 0


p = puzzle.Puzzle("16")
p.run(onetwo, 0)
# p.run(two, 0)
