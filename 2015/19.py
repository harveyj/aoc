#!/usr/bin/env python3
import puzzle
import re
import networkx as nx

def parse(INPUT):
  rules_raw, start = '\n'.join(INPUT).split("\n\n")
  pat = re.compile('(\w+) => (\w+)')
  rules = []
  for l in rules_raw.split('\n'):
    mat = re.match(pat, l).groups()
    rules.append((mat[0], mat[1]))
  return rules, start

def one(INPUT):
  rules, begin_str = parse(INPUT)
  # print(rules, begin_str)
  outs = set()
  for r in rules:
    loc = 0
    while True:
      new_loc = begin_str.find(r[0], loc)
      if new_loc == -1: break
      outs.add(begin_str[:new_loc] + r[1] + begin_str[new_loc+len(r[0]):])
      loc = new_loc+1
  # print(outs, len(outs))
  return len(outs)

def two(INPUT):
  rules, molecule = parse(INPUT)
  for i in range(500):
    # print(molecule)
    if molecule == "e":
      return i
    for r in rules:
      new_loc = molecule.find(r[1])
      if new_loc == -1:
        continue
      else:
        molecule = molecule[:new_loc] + r[0] + molecule[new_loc+len(r[1]):]
        break
  return 0

p = puzzle.Puzzle("2015", "19")
p.run(one, 0)
p.run(two, 0)
