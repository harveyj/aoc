#!/usr/bin/env python3
import puzzle

def code(char):
  if char.islower():
    return ord(char.upper()) - 64
  else:
    return ord(char.lower()) - 70


def code(char):
  if char.islower():
    return ord(char.upper()) - 64
  else:
    return ord(char.lower()) - 70

def one(INPUT):
  total = 0
  for l in INPUT.split('\n'):
    l_1 = set(l[:len(l)//2])
    l_2 = set(l[len(l)//2:])
    # print(l_1, l_2)
    intersect = l_1.intersection(l_2)
    total += code(list(intersect)[0])

  return total

def two(INPUT):
  total = 0
  lines = INPUT.split('\n')
  for i in range(len(lines)//3):
    base_i = i*3
    badge = set(lines[base_i]).intersection(lines[base_i+1]).intersection(lines[base_i+2])
    total += code(list(badge)[0])

  return total

p = puzzle.Puzzle("3")
p.run(one, 0)
p.run(two, 0)
