#!/usr/bin/env python3
import puzzle, re, library
from collections import defaultdict
import networkx as nx

def parse_input(INPUT):
  for l in INPUT:
    yield l.split()[1], l.split()[7]

def one(INPUT):
  DG = nx.DiGraph()
  for a, b in parse_input(INPUT):
    DG.add_edge(a, b)
  out = []
  while len(out) < len(DG):
    unvisited = [n for n in DG if n not in out]
    ready = [n for n in unvisited if len([i_e for i_e in DG.in_edges(n) if i_e[0] in unvisited]) == 0]
    ready.sort()
    out += ready[0]
  return ''.join(out)

TIMES = zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ', range(1, 27))
TIMES = {char: t+60 for (char, t) in TIMES}

def two(INPUT):
  DG = nx.DiGraph()
  for a, b in parse_input(INPUT):
    DG.add_edge(a, b)
  done = []
  pending = []
  time = 0
  while len(done) < len(DG):
    done += [code for (code, t) in pending if t == 1]
    pending = [(code, t-1) for (code, t) in pending if t > 1]
    if len(pending) < 4:
      unvisited = [n for n in DG if n not in done and n not in [p[0] for p in pending]]
      undone = [n for n in DG if n not in done]
      ready = [n for n in unvisited if len([i_e for i_e in DG.in_edges(n) if i_e[0] in undone]) == 0]
      ready = sorted(ready)[::-1]
      while len(pending) < 5 and ready:
        new = ready.pop()
        pending.append((new, TIMES[new]))
    time += 1
  return time-1 # undo last +1 in while loop

if __name__ == '__main__':
  p = puzzle.Puzzle("2018", "7")
  print(p.run(one, 0))
  print(p.run(two, 0))