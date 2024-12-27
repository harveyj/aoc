#!/usr/bin/env python3
import puzzle
import networkx as nx

def one(INPUT):
  G = nx.Graph()
  for l in INPUT:
    a, b = l.split('-')
    G.add_edge(a, b)
  clusters = []
  for clique in [clique for clique in nx.enumerate_all_cliques(G)]:
    if len(clique) == 3:
      if [c for c in clique if c[0] == 't']:
        clusters.append(clique)
  return len(clusters)

def two(INPUT):
  G = nx.Graph()
  for l in INPUT:
    a, b = l.split('-')
    G.add_edge(a, b)
  cliques = [(len(clique), clique) for clique in nx.find_cliques(G)]
  max_clique = sorted(cliques)[-1][1]
  return '-'.join(sorted(max_clique))

if __name__ == '__main__':
  p = puzzle.Puzzle("2024", "23")
  print(f'ANSWER: {p.run(one, 0)}')
  print(f'ANSWER: {p.run(two, 0)}')