#!/usr/bin/env python3
import puzzle
import networkx
import re
import itertools

def parse(INPUT):
  pat = re.compile('(\w+) would .* (\d+) happiness units by sitting next to (\w+).')
  for l in INPUT:
    # print(l)
    a, delta, b = re.match(pat, l).groups()
    delta = int(delta)
    if "lose" in l: delta *= -1
    yield a, delta, b


def onetwo(INPUT):
  G = networkx.DiGraph()
  for a, delta, b in parse(INPUT):
    G.add_edge(a, b, weight=delta)
  max_happiness_order = None
  max_happiness_val = -100000000000
  for order in itertools.permutations(G.nodes):
    total = 0; prev = None
    for person in order:
      if prev:
        total += G.get_edge_data(prev, person)['weight']
        total += G.get_edge_data(person, prev)['weight']
      prev = person
    total += G.get_edge_data(prev, order[0])['weight']
    total += G.get_edge_data(order[0], prev)['weight']
    if total > max_happiness_val:
      max_happiness_order = order
      max_happiness_val = total
  return max_happiness_val

def one(INPUT):
  return puzzle.Puzzle("2015", "13").run(onetwo, 1)
def two(INPUT):
  return puzzle.Puzzle("2015", "13").run(onetwo, 0)

if __name__ == '__main__':
  p = puzzle.Puzzle("2015", "13")
  p.run(one, -1)
  p.run(two, -1)
