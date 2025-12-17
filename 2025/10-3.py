#!/usr/bin/env python3
import puzzle, re, library
import networkx as nx
import itertools
from scipy.optimize import minimize

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

def button_presses(buttons, joltage_i):
  return {'type': 'eq',
          'fun': lambda v: sum([v[i] if i in button else 0 for i, button in enumerate(buttons)]) - joltage_i}
      

def two(INPUT):
  total = 0

  for _, buttons, joltage in list(parse_input(INPUT)):
    print()
    print('tgt', joltage)
    gt = [
      {'type': 'ineq','fun': lambda v: v[b_idx]}  # bi >= 0
      for b_idx, _ in enumerate(buttons)
    ]
    equations = [button_presses(buttons, joltage_i) for joltage_i in joltage]
    print(gt + equations)
    res = minimize(sum, x0=[0 for b_idx in range(len(buttons))], constraints=gt + equations, method="SLSQP")

    for e in equations: print(e['fun'](res.x))
    print(res.success, res.message)

    print(res.x, res.fun)


  return total

if __name__ == '__main__':
  p = puzzle.Puzzle("2025", "10")
  # print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')
