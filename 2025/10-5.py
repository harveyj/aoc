#!/usr/bin/env python3
import puzzle, re, library, copy
import networkx as nx
import itertools
import sympy as sp

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
  for tgt_lights, buttons, _ in list(parse_input(INPUT)):
    G = nx.DiGraph()
    S = tuple('.'*len(tgt_lights))
    E = tuple(tgt_lights)
    for state in itertools.product('.#', repeat=len(tgt_lights)):
      for button in buttons:
        new_state = [flip(c) if i in button else c for i, c in enumerate(state)]
        G.add_edge(tuple(state), tuple(new_state))
    ans += (nx.shortest_path_length(G, S, E))
  return ans

def find_valid(sol_set, valids):
  
  sign = sp.diff(sum(sol_set), fv) > 0
  selected = valids[0] if sign else valids[-1]
  sol_set = sol_set.subs(fv, selected)

  pass

from z3 import *


def two(INPUT):
  total = 0

  for _, buttons, joltage in list(parse_input(INPUT)):
    print()
    print('tgt', joltage)
    opt = Optimize()
    button_presses = IntVector('b', len(buttons))
    opt.add(*[bp >= 0 for bp in button_presses])

    all_eqs = []
    for i in range(len(joltage)):
      all_eqs.append([button_presses[j] for j, button in enumerate(buttons) if i in button])
    for eq, jolt in list(zip(all_eqs, joltage)): 
      # print(eq, jolt)
      opt.add(Sum(*eq) == jolt)
    all_presses = Sum(button_presses)
    # print(opt)
    opt.minimize(all_presses)
    res = opt.check()
    assert res == sat
    m = opt.model()
    # print(all_presses)
    print("obj:", m.eval(all_presses, model_completion=True))
    print("vars:", [m.eval(bp, model_completion=True) for bp in button_presses])
    total += m.eval(all_presses, model_completion=True).as_long()
  return total

if __name__ == '__main__':
  p = puzzle.Puzzle("2025", "10")
  # print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')
