#!/usr/bin/env python3
import puzzle
import networkx as nx
from functools import lru_cache

@lru_cache()
def count_paths(DG, src, dst):
  if src == dst:
    return 1
  return sum([count_paths(DG, node, dst) for node in DG.successors(src)])

def one(INPUT, two=False):
  DG = nx.DiGraph()
  nodes = []
  for l in INPUT:
    fields = l.split()
    fields[0] = fields[0][:-1] # strip colon
    nodes.append(fields)
  for node in nodes:
    for dst in node[1:]:
      DG.add_edge(node[0], dst)

  if two:
    # no paths fft-dac in my input. route must be svr-dac-fft-out
    return count_paths(DG, "svr", "fft") * count_paths(DG, "fft", "dac") * count_paths(DG, "dac", "out") 
  return len(list(nx.all_simple_paths(DG, 'you', 'out')))

def two(INPUT):
  return one(INPUT, two=True)

if __name__ == '__main__':
  p = puzzle.Puzzle("2025", "11")
  # print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')
