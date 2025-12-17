#!/usr/bin/env python3
import puzzle, re, library
import networkx as nx
import itertools
from functools import partial

def parse_input(INPUT):
  for l in INPUT:
    chunks = l.split()
    tgt_lights, schematics_raw, joltage = chunks[0][1:-1], chunks[1:-1], library.ints(chunks[-1])
    buttons = [library.ints(raw) for raw in schematics_raw]
    yield tgt_lights, buttons, joltage

def flip(c):
  return "#" if c == "." else "."

def one(INPUT):
  ans = 0
  for tgt_lights, buttons, joltage in list(parse_input(INPUT)):
    G = nx.DiGraph()
    S = tuple('.'*len(tgt_lights))
    E = tuple(tgt_lights)
    for state in itertools.product('.#', repeat=len(tgt_lights)):
      for button in buttons:
        new_state = [flip(c) if i in button else c for i, c in enumerate(state)]
        G.add_edge(tuple(state), tuple(new_state))
    ans += (nx.shortest_path_length(G, S, E))
  return ans

def h(max_per_press, tgt, state):
  return sum([a-b for a, b in zip(tgt, state)]) // max_per_press

def neighbors(tgt, buttons, current):
  for b in buttons:
    out = tuple(c + (1 if i in b else 0) for i, c in enumerate(current))
    over = [o for o, t in zip(out, tgt) if o > t]
    if len(over) == 0: 
      yield out

def two(INPUT):
  total = 0
  for _, buttons, joltage in list(parse_input(INPUT)):
    print('.')
    start = tuple([0]*len(joltage))
    goal = tuple(joltage)
    max_per_press = max([len(b) for b in buttons])
    path = library.a_star_lazy(start, goal, 
                        partial(h, max_per_press, joltage), 
                        partial(neighbors, joltage, buttons))
    total += len(path[1:])  # it's button presses, so first one doesn't count 
  return total

if __name__ == '__main__':
  p = puzzle.Puzzle("2025", "10")
  # print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')
