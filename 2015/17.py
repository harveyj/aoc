#!/usr/bin/env python3
import puzzle
import itertools

def parse(INPUT):
  return map(int, INPUT)


def onetwo(INPUT, two=False):
  buckets = list(parse(INPUT))
  combos = 0
  for i in range(len(buckets)):
    if two and combos > 0:
      break
    for combo in itertools.combinations(buckets, i):
      if sum(combo) == 150:
        combos += 1
  return combos

def one(INPUT): return onetwo(INPUT, two=False)
def two(INPUT): return onetwo(INPUT, two=True)

p = puzzle.Puzzle("2015", "17")
p.run(one, 0)
p.run(two, 0)
