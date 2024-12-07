#!/usr/bin/env python3
import puzzle
import re

def parse(INPUT):
  pat = re.compile('(\w+)+')
  for l in INPUT:
    yield re.match(pat, l).groups()


def one(INPUT):
  for l in INPUT:
    canceled_l = re.sub('!.', '', l)
    processed_l = re.sub('<.*?>', '', canceled_l)
    depth = 0; total = 0
    for c in processed_l:
      if c == '{':
        depth += 1
      if c == '}':
        total += depth
        depth -= 1
    return total

def two(INPUT):
  for l in INPUT:
    canceled_l = re.sub('!.', '', l)
    processed_l = re.sub('<.*?>', '<>', canceled_l)
    return len(canceled_l) - len(processed_l)

if __name__ == '__main__':
  p = puzzle.Puzzle("2017", "9")

  p.run(one, 0)
  p.run(two, 0)
