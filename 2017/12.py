#!/usr/bin/env python3
import puzzle
import re
import networkx as nx

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

def one(INPUT):
  return onetwo(INPUT)[0]
def two(INPUT):
  return onetwo(INPUT)[1]

if __name__ == '__main__':
  p = puzzle.Puzzle("2017", "12")
  p.run(one, 0)
  p.run(two, 0)
