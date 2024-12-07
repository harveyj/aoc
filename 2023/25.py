#!/usr/bin/env python3
import puzzle, re, networkx as nx

def parse_input(INPUT):
  G=nx.Graph()
  for l in INPUT:
    lval, rval = l.split(':')
    rval = rval.strip().split()
    G.add_node(lval)
    for rv in rval: 
      G.add_edge(lval, rv)
      G.add_node(rv)

  return G

def one(INPUT):
  G = parse_input(INPUT)
  ec = nx.minimum_edge_cut(G)
  for edge in ec:
    G.remove_edge(*edge)
  answer = 1
  for sg in nx.k_edge_subgraphs(G, k=1):
    answer *= len(sg)
  return answer


def two(INPUT):
  invals = parse_input(INPUT)
  out = 0
  return out

if __name__ == '__main__':
  p = puzzle.Puzzle("2023", "25")

  p.run(one, 0) 
  p.run(two, 0) 
