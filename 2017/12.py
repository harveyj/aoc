#!/usr/bin/env python3
import puzzle, library
import re
import networkx as nx
from collections import defaultdict

def parse(INPUT):
  pat = re.compile('(\d+) <-> (.*)')
  for l in INPUT:
    gr = re.match(pat, l)
    yield int(gr[1]), list(map(int, gr[2].split(',')))


def onetwo(INPUT):
  G = nx.Graph()
  for n, out_list in (parse(INPUT)):
    # print(n, out_list)
    for on in out_list:
      # print(n, on)
      G.add_edge(n, on) 
  cc = nx.connected_components(G)
  for c in cc:
    if 0 in c:
      return len(c), len(list(nx.connected_components(G)))

def two(INPUT):
  return 0

p = puzzle.Puzzle("2017", "12")
p.run(onetwo, 0)
