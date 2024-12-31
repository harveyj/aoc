#!/usr/bin/env python3
import puzzle, re, library
from collections import deque

def parse_input(INPUT):
  return INPUT

def one(INPUT):
  seed = int(INPUT[0])
  elf1, elf2 = (0, 1)
  recipes = [3, 7]
  for i in range(seed+10):
    new = recipes[elf1] + recipes[elf2]
    if new > 9:
      recipes.append(new // 10)
    recipes.append(new % 10)
    elf1 = (1+ elf1 + recipes[elf1]) % len(recipes)
    elf2 = (1+ elf2 + recipes[elf2]) % len(recipes)
  last10 = recipes[seed:seed+10]
  return ''.join([str(a) for a in last10])

def two(INPUT):
  seed = INPUT[0]
  elf1, elf2 = (0, 1)
  recipes = [3, 7]
  for i in range(100000000):
    new = recipes[elf1] + recipes[elf2]
    if new > 9:
      recipes.append(new // 10)
    if ''.join(map(str, recipes[-len(seed):])) == seed:
      return len(recipes) - len(seed)
    recipes.append(new % 10)
    if ''.join(map(str, recipes[-len(seed):])) == seed:
      return len(recipes) - len(seed)
    elf1 = (1+ elf1 + recipes[elf1]) % len(recipes)
    elf2 = (1+ elf2 + recipes[elf2]) % len(recipes)

if __name__ == '__main__':
  p = puzzle.Puzzle("2018", "14")
  print(p.run(one, 0))
  print(p.run(two, 0))