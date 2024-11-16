#!/usr/bin/env python3
import puzzle
import itertools

def parse(INPUT):
  return map(int, INPUT.split('\n'))


def one(INPUT):
  buckets = list(parse(INPUT))
  combos = 0
  for i in range(len(buckets)):
    if combos > 0:
      break
    for combo in itertools.combinations(buckets, i):
      # print(combo)
      if sum(combo) == 150:
        combos += 1
        # print(combo)
  return combos

def two(INPUT):
  return 0

p = puzzle.Puzzle("2015", "17")
p.run(one, 0)
# p.run(two, 0)
