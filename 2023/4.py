#!/usr/bin/env python3
import puzzle

def parse_input(INPUT):
  lines = INPUT.split('\n')
  parsed = [(l.split(":")[1].split('|')[0], l.split('|')[1]) for l in lines]
  processed = [(list(map(int, p[0].split())), list(map(int, p[1].split()))) for p in parsed]
  return processed

def one(INPUT):
  lines = parse_input(INPUT)
  out = 0
  for inval in lines:
    overlap = set(inval[0]).intersection(set(inval[1]))
    if overlap:
      out += 2**(len(overlap)-1)
  return out

def two(INPUT):
  lines = parse_input(INPUT)
  out = 0
  values = dict()
  links = dict()
  for i, inval in enumerate(lines):
    overlap = set(inval[0]).intersection(set(inval[1]))
    if len(overlap) == 0:
      values[i] = 1
    links[i] = range(i+1, i+len(overlap)+1)
  while len(values) < len(lines):
    print(links)
    for i, links_i in links.items():
      total = 1
      print(links_i)
      for link_idx in links_i:
        if link_idx in values:
          total += values[link_idx]
        else:
          break
      if total > 1:
        values[i] = total
  print(values)
  print(links)
  out = 0
  for i in values.values():
    out += i
  return out

p = puzzle.Puzzle("4")
p.run(one, 0)
p.run(two, 0)

for a in range(4, 4): print(a)