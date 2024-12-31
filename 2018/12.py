#!/usr/bin/env python3
import puzzle, library
from collections import defaultdict
import itertools

def parse_input(INPUT):
  chunks = '\n'.join(INPUT).split('\n\n')
  state = chunks[0].split()[2]
  rules = [a.split() for a in chunks[1].split('\n')]
  rules = {tuple([1 if c == '#' else 0 for c in lval]): 1 if rval == '#' else 0 for (lval, _, rval) in rules}
  return rules, state

def iter(rules, state):
  pots = defaultdict(int)
  for i, pot in enumerate(state):
    pots[i] = 1 if pot == '#' else 0
  min_key = min(pots.keys())
  max_key = max(pots.keys())
  for i in range(1, 1000000000):
    min_key -= 2
    max_key += 2
    new_pots = defaultdict(int)
    for pot_idx in range(min_key, max_key):
      surrounds = tuple([pots[idx] for idx in range(pot_idx -2, pot_idx + 3)])
      new_pots[pot_idx] = rules[surrounds]
    pots = new_pots
    yield i, pots

def score(pots):
  return sum([key for key in pots.keys() if pots[key] == 1])

def one(INPUT):
  rules, state = parse_input(INPUT)
  ITERS = 20
  for (i, pots) in iter(rules, state):
    if i == ITERS:
      break
  return score(pots)

def two(INPUT):
  rules, state = parse_input(INPUT)
  i, offset, delt = library.detect_steady_state(iter(rules, state), score)
  return offset + (50000000000 - i) * delt

if __name__ == '__main__':
  p = puzzle.Puzzle("2018", "12")
  print(p.run(one, 0))
  print(p.run(two, 0))