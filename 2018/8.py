#!/usr/bin/env python3
import puzzle, re, library
from collections import defaultdict
import networkx as nx

def parse_tree(DG, array, a):
  DG.add_node(a, metadata=[])
  child_nodes, metadata_entries = array[a], array[a+1]
  idx = a + 2 # always consume the first two items (see above)
  for i in range(child_nodes):
    DG.add_edge(a, idx)
    idx += parse_tree(DG, array, idx)
  for i in range(metadata_entries):
    DG.nodes[a]['metadata'].append(array[idx])
    idx += 1
  return idx-a

def one(INPUT):
  DG = nx.DiGraph()
  invals = library.ints(INPUT[0])
  parse_tree(DG, invals, 0)
  out = 0
  for n in DG.nodes():
    if 'metadata' in DG.nodes[n]:
      out += sum(DG.nodes[n]['metadata'])
  return out

def two(INPUT):
  DG = nx.DiGraph()
  invals = library.ints(INPUT[0])
  parse_tree(DG, invals, 0)
  vals = {}
  for n in nx.dfs_postorder_nodes(DG, source=0):
    children = list(DG.successors(n))
    if len(children) > 0:
      vals[n] = sum([vals[children[i-1]] for i in DG.nodes[n]['metadata'] if i-1 < len(children)])
    else:
      total = sum(DG.nodes[n]['metadata'])
      vals[n] = total # if 'metadata' in DG.nodes[n] else [0]])
  return vals[0]

if __name__ == '__main__':
  p = puzzle.Puzzle("2018", "8")
  print(p.run(one, 0))
  print(p.run(two, 0))