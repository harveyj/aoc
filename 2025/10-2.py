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

def two(INPUT):
  total = 0

  for _, buttons, joltage in list(parse_input(INPUT)):
    print()
    print('tgt', joltage)
    A = sp.Matrix([[1 if i in button else 0 for i in range(len(joltage))] for button in buttons])
    b = sp.Matrix(joltage)
    button_presses = sp.symbols(f'b0:{len(buttons)}')
    sol_set = list(sp.linsolve((A.T, b), list(button_presses)))[0]
    free = list(sol_set.free_symbols)
    partial_derivs = [(sp.diff(sum(sol_set), fv), fv) for fv in free]
    abs_partial_derivs = sorted([(((abs(pd) + 0.1) if pd > 0 else abs(pd)), fv) for pd, fv in partial_derivs], key=lambda a:a[0], reverse=True)
    print(abs_partial_derivs)
    print('sum', sum(sol_set))
    proposed = copy.copy(sol_set)
    for _, fv in abs_partial_derivs:
      constraints = ([eq >= 0 for eq in sol_set])
      result = sp.reduce_inequalities(constraints, fv)
      print('res', result)
      valids = [j for j in range(1000) if result.subs(fv, j)]
      print('valids ', fv, valids)

      # sign = sp.diff(sum(sol_set), fv) > 0
      # selected = valids[0] if sign else valids[-1]
      # sol_set = sol_set.subs(fv, selected)

    total += sum(sol_set)
  return total

if __name__ == '__main__':
  p = puzzle.Puzzle("2025", "10")
  # print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')
