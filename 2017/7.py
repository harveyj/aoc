#!/usr/bin/env python3
import puzzle, library
import re
import networkx as nx
import hashlib
from collections import defaultdict


def parse(INPUT):
  pat = re.compile('(\w+) \((\d+)\)( -> )?(.*)?')
  for l in INPUT:
    yield re.match(pat, l).groups()


def one(INPUT):
  G = nx.DiGraph()
  for node in parse(INPUT):
    src, val = node[0], int(node[1])
    outs = node[3].split(',') if node[3] else []
    for o in outs:
      G.add_edge(src, o.strip())
  for n in G.nodes:
    if G.in_degree(n) == 0:
      return n

def two(INPUT):
  G = nx.DiGraph()
  vals = dict()
  aggregate_vals = defaultdict(int)
  start = one(INPUT)
  for node in parse(INPUT):
    src, val = node[0], int(node[1])
    vals[src] = val
    outs = node[3].split(',') if node[3] else []
    for o in outs:
      G.add_edge(src, o.strip())
  for n in reversed(list(nx.topological_sort(G))):
    ins = list(G.in_edges(n))
    aggregate_vals[n] += vals[n]
    if len(ins):
      in_key = list(G.in_edges(n))[0][0]
      aggregate_vals[in_key] += aggregate_vals[n]
  # print(aggregate_vals)
  n = start
  # n='tknk'
  for i in range(10):
    all_out_vals = defaultdict(list)
    for _, out in G.out_edges(n):
      all_out_vals[aggregate_vals[out]].append(out)
    uniques = [all_out_vals[out] for out in all_out_vals if len(all_out_vals[out]) == 1]
    if len(uniques) == 1: n = uniques[0]
    else:
      # print('FOUND', n[0])
      parent = list(G.in_edges(n))[0][0]
      children = [oe[1] for oe in G.out_edges(parent) if oe[1] != n[0]]
      return vals[n[0]] + aggregate_vals[children[0]] - aggregate_vals[n[0]]   

if __name__ == '__main__':
  p = puzzle.Puzzle("2017", "7")

  p.run(one, 0)
  p.run(two, 0)
